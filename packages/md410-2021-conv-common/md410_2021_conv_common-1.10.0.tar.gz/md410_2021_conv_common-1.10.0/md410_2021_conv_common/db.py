from collections import defaultdict
from datetime import datetime
from decimal import Decimal, getcontext
import os

import attr
import sqlalchemy as sa

# permit use in both a package and standalone for testing purposes.
# See https://stackoverflow.com/questions/14132789/relative-imports-for-the-billionth-time/14132912#14132912
if __package__:
    from . import constants
else:
    import constants

getcontext().prec = 20
TWOPLACES = Decimal(10) ** -2

TABLES = {
    "registree": ("md410_2021_conv", "registree"),
    "club": ("md410_2021_conv", "club"),
    "partner_program": ("md410_2021_conv", "partner_program"),
    "full_reg": ("md410_2021_conv", "full_reg"),
    "partial_reg": ("md410_2021_conv", "partial_reg"),
    "pins": ("md410_2021_conv", "pins"),
    "registree_pair": ("md410_2021_conv", "registree_pair"),
    "payment": ("md410_2021_conv", "payment"),
    "2020_registree": ("md410_2020_conv", "registree"),
    "2020_registree_pair": ("md410_2020_conv", "registree_pair"),
    "2020_payment": ("md410_2020_conv", "payment"),
}


@attr.s
class RegistreeSet(object):
    reg_num = attr.ib()
    events = attr.ib()
    extras = attr.ib()
    registrees = attr.ib()
    payments = attr.ib(default=[])

    def __attrs_post_init__(self):
        self.reg_num = int(self.reg_num)
        self.reg_num_text = f"MDC{self.reg_num:03}"
        self.cost = self.events.cost + self.extras.cost
        self.process_payments()
        self.registree_names = " and ".join(reg.name for reg in self.registrees)
        self.registree_first_names = " and ".join(
            reg.titled_first_names for reg in self.registrees
        )
        file_name_names = "_".join(
            f"{reg.first_names[0].lower()}_{reg.last_name.replace(' ','_').lower()}"
            for reg in self.registrees
        )
        self.file_name = f"{self.reg_num:003}_{file_name_names}"
        self.deposit = constants.DEPOSIT * len(self.registrees)

    def process_payments(self):
        self.paid = Decimal(sum(p.amount for p in self.payments))
        self.paid_in_full = self.paid >= self.cost
        self.still_owed = self.cost - self.paid


@attr.s
class Events(object):
    full = attr.ib()
    banquet = attr.ib()
    convention = attr.ib()
    theme = attr.ib()
    costs = attr.ib(
        default={
            "full": constants.COST_EVENT_FULL,
            "banquet": constants.COST_EVENT_BANQUET,
            "convention": constants.COST_EVENT_CONVENTION,
            "theme": constants.COST_EVENT_THEME,
        }
    )

    def __attrs_post_init__(self):
        self.cost = Decimal(sum(self.get_costs_per_item().values()))
        self.includes_full = self.full > 0
        self.includes_partial = any(
            getattr(self, attr) > 0 for attr in ("banquet", "convention", "theme")
        )

    def get_costs_per_item(self):
        return {attr: cost * getattr(self, attr) for (attr, cost) in self.costs.items()}


@attr.s
class Payment(object):
    timestamp = attr.ib()
    amount = attr.ib()


@attr.s
class Extras(object):
    pins = attr.ib()
    costs = attr.ib(default={"pins": constants.COST_EXTRAS_PIN})

    def __attrs_post_init__(self):
        self.cost = Decimal(sum(self.get_costs_per_item().values()))

    def get_costs_per_item(self):
        return {attr: cost * getattr(self, attr) for (attr, cost) in self.costs.items()}

    def __bool__(self):
        return bool(sum([getattr(self, attr) for attr in self.costs.keys()]))


@attr.s
class Registree(object):
    timestamp = attr.ib()
    first_names = attr.ib()
    last_name = attr.ib()
    cell = attr.ib()
    email = attr.ib()
    dietary = attr.ib()
    disability = attr.ib()
    name_badge = attr.ib()
    title = attr.ib()
    first_mdc = attr.ib()
    mjf_lunch = attr.ib()

    def __attrs_post_init__(self):
        if not self.title:
            self.title = None
        t = f"{self.title} " if self.title else ""
        self.titled_first_names = f"{t}{self.first_names.strip()}"
        self.name = f"{self.titled_first_names} {self.last_name}"

        self.auto_name_badge = False
        if not self.name_badge:
            self.name_badge = f"{self.first_names} {self.last_name}"
            self.auto_name_badge = True


@attr.s
class LionRegistree(Registree):
    club = attr.ib()
    district = attr.ib()

    def __attrs_post_init__(self):
        self.lion = True
        super().__attrs_post_init__()


@attr.s
class NonLionRegistree(Registree):
    partner_program = attr.ib(default=0)

    def __attrs_post_init__(self):
        self.lion = False
        super().__attrs_post_init__()


@attr.s
class DB(object):
    """Handle postgres database interaction"""

    host = attr.ib(default=os.getenv("PGHOST", "localhost"))
    port = attr.ib(default=os.getenv("PGPORT", 5432))
    user = attr.ib(default=os.getenv("PGUSER", "postgres"))
    password = attr.ib(default=os.getenv("PGPASSWORD"))
    dbname = attr.ib(default="postgres")
    debug = attr.ib(default=False)

    def __attrs_post_init__(self):
        self.engine = sa.create_engine(
            f"postgresql+psycopg2://{self.user}:{self.password}@{self.host}:{self.port}/{self.dbname}",
            echo=self.debug,
        )
        md = sa.MetaData()
        md.bind = self.engine
        self.engine.autocommit = True
        self.tables = {}
        for (k, (schema, name)) in TABLES.items():
            self.tables[k] = sa.Table(name, md, autoload=True, schema=schema)
        self.reg_nums = []

    def get_registrees(self, reg_num):
        tr = self.tables["registree"]
        tc = self.tables["club"]
        tpy = self.tables["payment"]
        tpp = self.tables["partner_program"]
        tpi = self.tables["pins"]
        tfr = self.tables["full_reg"]
        tpr = self.tables["partial_reg"]

        partials = [
            sum(e)
            for e in zip(
                *[
                    p[:]
                    for p in self.engine.execute(
                        sa.select(
                            [
                                tpr.c.banquet_quantity,
                                tpr.c.convention_quantity,
                                tpr.c.theme_quantity,
                            ],
                            tpr.c.reg_num == reg_num,
                        )
                    ).fetchall()
                ]
            )
        ]
        if not partials:
            partials = [0, 0, 0]
        events = Events(
            *(
                [
                    sum(
                        r[0]
                        for r in self.engine.execute(
                            sa.select([tfr.c.quantity], tfr.c.reg_num == reg_num)
                        ).fetchall()
                    )
                ]
                + partials
            )
        )

        payments = [
            Payment(p[0], p[1])
            for p in self.engine.execute(
                sa.select([tpy.c.timestamp, tpy.c.amount], tpy.c.reg_num == reg_num)
            ).fetchall()
        ]

        extras = Extras(
            pins=sum(
                p[0]
                for p in self.engine.execute(
                    sa.select([tpi.c.quantity], tpi.c.reg_num == reg_num)
                ).fetchall()
            )
        )

        res = self.engine.execute(
            sa.select(
                [
                    tr.c.timestamp,
                    tr.c.first_names,
                    tr.c.last_name,
                    tr.c.cell,
                    tr.c.email,
                    tr.c.dietary,
                    tr.c.disability,
                    tr.c.name_badge,
                    tr.c.title,
                    tr.c.first_mdc,
                    tr.c.mjf_lunch,
                    tr.c.is_lion,
                    tr.c.id,
                ],
                whereclause=sa.and_(
                    tr.c.reg_num == reg_num, tr.c.cancellation_timestamp == None
                ),
            )
        ).fetchall()
        registrees = []
        for r in res:
            vals = r[:-2]
            if r.is_lion:
                details = self.engine.execute(
                    sa.select([tc.c.club, tc.c.district], tc.c.registree_id == r.id)
                ).fetchone()
                cls = LionRegistree
            else:
                details = self.engine.execute(
                    sa.select([tpp.c.quantity], tpp.c.registree_id == r.id)
                ).fetchone()
                if not details:
                    details = (0,)
                cls = NonLionRegistree
            registrees.append(cls(*(vals + details[:])))

        return RegistreeSet(reg_num, events, extras, registrees, payments)

    def save_registree_set(self, registree_set):
        tr = self.tables["registree"]
        tfr = self.tables["full_reg"]
        tpr = self.tables["partial_reg"]
        tpi = self.tables["pins"]
        tpp = self.tables["partner_program"]
        tc = self.tables["club"]
        tp = self.tables["payment"]
        for t in (tr, tc, tpp, tfr, tpr, tpi):
            self.engine.execute(t.delete(t.c.reg_num == registree_set.reg_num))

        for registree in registree_set.registrees:
            d = {
                "is_lion": registree.lion,
                "reg_num": registree_set.reg_num,
                "first_names": registree.first_names,
                "last_name": registree.last_name,
                "cell": registree.cell,
                "email": registree.email,
                "dietary": registree.dietary,
                "disability": registree.disability,
                "name_badge": registree.name_badge,
                "title": registree.title,
                "first_mdc": registree.first_mdc,
                "mjf_lunch": registree.mjf_lunch,
                "timestamp": registree.timestamp,
            }
            registree_id = self.engine.execute(tr.insert(d).returning(tr.c.id)).scalar()
            if registree.lion:
                self.engine.execute(
                    tc.insert(
                        {
                            "reg_num": registree_set.reg_num,
                            "club": registree.club,
                            "district": registree.district,
                            "registree_id": registree_id,
                        }
                    )
                )
            else:
                self.engine.execute(
                    tpp.insert(
                        {
                            "reg_num": registree_set.reg_num,
                            "quantity": registree.partner_program,
                            "registree_id": registree_id,
                        }
                    )
                )

        payments = [
            {
                "reg_num": registree_set.reg_num,
                "amount": payment.amount,
                "timestamp": payment.timestamp,
            }
            for payment in registree_set.payments
        ]
        if payments:
            self.engine.execute(tp.insert(payments))

        if registree_set.extras.pins:
            self.engine.execute(
                tpi.insert(
                    {
                        "reg_num": registree_set.reg_num,
                        "quantity": registree_set.extras.pins,
                    }
                )
            )

        if registree_set.events.includes_full:
            self.engine.execute(
                tfr.insert(
                    {
                        "reg_num": registree_set.reg_num,
                        "quantity": registree_set.events.full,
                    }
                )
            )

        if registree_set.events.includes_partial:
            self.engine.execute(
                tpr.insert(
                    {
                        "reg_num": registree_set.reg_num,
                        "banquet_quantity": registree_set.events.banquet,
                        "convention_quantity": registree_set.events.convention,
                        "theme_quantity": registree_set.events.theme,
                    }
                )
            )

    # -----------------------------------------------------------------------

    def get_all_registrees(self, reg_nums=None):
        tr = self.tables["registree"]
        tfr = self.tables["full_reg"]
        tpr = self.tables["partial_reg"]
        tpi = self.tables["pins"]
        tpy = self.tables["payment"]
        tc = self.tables["club"]

        query = sa.select(
            [
                tr.c.reg_num,
                tr.c.first_names,
                tr.c.last_name,
                tr.c.cell,
                tr.c.email,
                tr.c.is_lion,
            ]
        )

        if reg_nums:
            query = query.where(
                sa.and_(tr.c.reg_num.in_(reg_nums), tr.c.cancellation_timestamp == None)
            )
        else:
            query = query.where(tr.c.cancellation_timestamp == None)
        res = self.engine.execute(query).fetchall()
        registrees = []
        for r in res:
            d = dict(r)
            if r.is_lion:
                try:
                    d["club"] = self.engine.execute(
                        tc.select(whereclause=tc.c.reg_num == d["reg_num"])
                    ).fetchone()[1]
                except Exception:
                    pass
            try:
                d["full_regs"] = self.engine.execute(
                    tfr.select(whereclause=tfr.c.reg_num == d["reg_num"])
                ).fetchone()[1]
            except Exception:
                pass
            try:
                partial = self.engine.execute(
                    tpr.select(whereclause=tpr.c.reg_num == d["reg_num"])
                ).fetchone()
                d["banquets"] = partial["banquet_quantity"]
                d["conventions"] = partial["convention_quantity"]
                d["themes"] = partial["theme_quantity"]
            except Exception:
                pass

            try:
                d["pins"] = self.engine.execute(
                    tpi.select(whereclause=tpi.c.reg_num == d["reg_num"])
                ).fetchone()[1]
            except Exception:
                pass

            try:
                d["payments"] = sum(
                    p.amount
                    for p in self.engine.execute(
                        tpy.select(whereclause=tpy.c.reg_num == d["reg_num"])
                    ).fetchall()
                )
            except Exception:
                pass
            registrees.append(Registree(**d))
        return registrees

    def set_reg_nums(self, reg_num):
        tp = self.tables["registree_pair"]
        res = self.engine.execute(
            sa.select(
                [tp.c.first_reg_num, tp.c.second_reg_num],
                sa.or_(tp.c.first_reg_num == reg_num, tp.c.second_reg_num == reg_num),
            )
        ).fetchone()
        self.reg_nums = [res[0], res[1]] if res else [reg_num]

    def record_payment(self, amount, timestamp):
        tp = self.tables["payment"]
        amt = Decimal(amount).quantize(TWOPLACES) / (len(self.reg_nums))
        for rn in self.reg_nums:
            d = {"timestamp": timestamp, "reg_num": rn, "amount": amt}
            res = self.engine.execute(tp.insert(d))

    def upload_registree(self, registree):
        tr = self.tables["registree"]
        tc = self.tables["club"]
        tpp = self.tables["partner_program"]
        tfr = self.tables["full_reg"]
        tpr = self.tables["partial_reg"]
        tp = self.tables["pins"]
        for t in (tr, tc, tpp, tfr, tpr, tp):
            self.engine.execute(t.delete(t.c.reg_num == registree.reg_num))

        vals = {
            k: getattr(registree, k)
            for k in (
                "reg_num",
                "timestamp",
                "first_names",
                "last_name",
                "cell",
                "email",
                "dietary",
                "disability",
                "name_badge",
                "first_mdc",
                "mjf_lunch",
                # "pdg_breakfast",
                "is_lion",
                # "sharks_board",
                # "golf",
                # "sight_seeing",
                # "service_project",
            )
        }
        self.engine.execute(tr.insert(vals))

        if registree.is_lion:
            vals = {
                "reg_num": registree.reg_num,
                "club": registree.club,
                "district": registree.district,
            }
            self.engine.execute(tc.insert(vals))
        else:
            vals = {"reg_num": registree.reg_num, "quantity": 1}
            self.engine.execute(tpp.insert(vals))

        if registree.full_reg:
            vals = {"reg_num": registree.reg_num, "quantity": registree.full_reg}
            self.engine.execute(tfr.insert(vals))

        if registree.partial_reg:
            vals = {
                "reg_num": registree.reg_num,
                "banquet_quantity": registree.partial_reg.banquet,
                "convention_quantity": registree.partial_reg.convention,
                "theme_quantity": registree.partial_reg.theme,
            }
            self.engine.execute(tpr.insert(vals))

        if registree.pins:
            vals = {"reg_num": registree.reg_num, "quantity": registree.pins}
            self.engine.execute(tp.insert(vals))

    def cancel_registration(self, reg_nums):
        tr = self.tables["registree"]
        trp = self.tables["registree_pair"]
        tc = self.tables["club"]
        tpp = self.tables["partner_program"]
        tfr = self.tables["full_reg"]
        tpr = self.tables["partial_reg"]
        tp = self.tables["pins"]
        for t in (tc, tfr, tpp, tpr, tp):
            self.engine.execute(t.delete(t.c.reg_num.in_(reg_nums)))
        self.engine.execute(trp.delete(trp.c.first_reg_num.in_(reg_nums)))

        dt = datetime.now()
        self.engine.execute(
            tr.update(tr.c.reg_num.in_(reg_nums), {"cancellation_timestamp": dt})
        )

    def pair_registrees(self, first_reg_num, second_reg_num):
        tp = self.tables["registree_pair"]
        self.engine.execute(tp.delete(tp.c.first_reg_num == first_reg_num))

        vals = {"first_reg_num": first_reg_num, "second_reg_num": second_reg_num}
        self.engine.execute(tp.insert(vals))

    def get_2020_payees(self):
        tr = self.tables["2020_registree"]
        trp = self.tables["2020_registree_pair"]
        tp = self.tables["2020_payment"]

        res = self.engine.execute(
            sa.select(
                [
                    tr.c.reg_num,
                    tr.c.first_names,
                    tr.c.last_name,
                    tp.c.amount,
                    tr.c.cancellation_timestamp,
                ],
                sa.and_(
                    tr.c.reg_num == tp.c.reg_num, tr.c.cancellation_timestamp == None
                ),
            ).order_by(tr.c.reg_num)
        ).fetchall()
        totals = defaultdict(float)
        names = {}
        for r in res:
            totals[r.reg_num] += r.amount
            names[r.reg_num] = f"{r.last_name}, {r.first_names}"

        return {r: (name, totals[r]) for (r, name) in names.items()}
