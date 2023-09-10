from sqlalchemy import ForeignKey, Column, Integer, String, MetaData
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

convention = {
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
}
metadata = MetaData(naming_convention=convention)

Base = declarative_base(metadata=metadata)

class Company(Base):
    __tablename__ = 'companies'

    id = Column(Integer(), primary_key=True)
    name = Column(String())
    founding_year = Column(Integer())

    # Relationship to Freebie
    freebies = relationship("Freebie", backref="company")

    def __repr__(self):
        return f'<Company {self.name}>'

    def give_freebie(self, dev, item_name, value):
        # Create a new Freebie instance associated with this company and the given dev
        freebie = Freebie(dev=dev, company=self, item_name=item_name, value=value)
        return freebie

    @classmethod
    def oldest_company(cls):
        # Return the Company instance with the earliest founding year
        return cls.query.order_by(cls.founding_year).first()

class Dev(Base):
    __tablename__ = 'devs'

    id = Column(Integer(), primary_key=True)
    name = Column(String())

    # Relationship to Freebie
    freebies = relationship("Freebie", backref="dev")

    def __repr__(self):
        return f'<Dev {self.name}>'

    def received_one(self, item_name):
        # Check if any of the freebies associated with the dev has the specified item_name
        return any(freebie.item_name == item_name for freebie in self.freebies)

    def give_away(self, other_dev, freebie):
        # Check if the freebie belongs to the dev who's giving it away
        if freebie.dev == self:
            freebie.dev = other_dev
            return True
        return False

class Freebie(Base):
    __tablename__ = 'freebies'

    id = Column(Integer(), primary_key=True)
    item_name = Column(String())
    value = Column(Integer())

    # Foreign keys
    dev_id = Column(Integer, ForeignKey('devs.id'))
    company_id = Column(Integer, ForeignKey('companies.id'))

    def __repr__(self):
        return f'<Freebie {self.item_name} from {self.company.name} to {self.dev.name}>'
