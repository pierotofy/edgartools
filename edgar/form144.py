from dataclasses import dataclass
from typing import Dict, List

import pandas as pd
from bs4 import BeautifulSoup, Tag
from rich import box
from rich.columns import Columns
from rich.console import Group
from rich.panel import Panel
from rich.table import Table

from edgar._party import Address
from edgar._party import Filer, Contact
from edgar._rich import repr_rich
from edgar._xml import child_text, child_values


@dataclass(frozen=True)
class SecuritiesInformation:
    """
          <securitiesInformation>
         <securitiesClassTitle>Common stock</securitiesClassTitle>
         <brokerOrMarketmakerDetails>
            <name>Virtu Financial</name>
            <address>
               <com:street1>One Liberty Plaza</com:street1>
               <com:street2>165 Broadway</com:street2>
               <com:city>New York</com:city>
               <com:stateOrCountry>NY</com:stateOrCountry>
               <com:zipCode>10006</com:zipCode>
            </address>
         </brokerOrMarketmakerDetails>
         <noOfUnitsSold>17087</noOfUnitsSold>
         <aggregateMarketValue>1282000.00</aggregateMarketValue>
         <noOfUnitsOutstanding>161514066</noOfUnitsOutstanding>
         <approxSaleDate>08/27/2022</approxSaleDate>
         <securitiesExchangeName>CHX</securitiesExchangeName>
      </securitiesInformation>
    """
    security_class: str
    units_sold: int
    aggregate_market_value: float
    units_outstanding: int
    approx_sale_date: str
    exchange_name: str
    broker_name: str
    broker_address: Address

    def to_dict(self):
        # Convert this object to a dictionary
        return {
            'security_class': self.security_class,
            'units_sold': self.units_sold,
            'market_value': self.aggregate_market_value,
            'units_outstanding': self.units_outstanding,
            'approx_sale_date': self.approx_sale_date,
            'exchange_name': self.exchange_name,
            'broker_name': self.broker_name
        }

    @classmethod
    def from_tag(cls, tag: Tag):
        security_class = child_text(tag, 'securitiesClassTitle')
        units_sold = child_text(tag, 'noOfUnitsSold')
        aggregate_market_value = child_text(tag, 'aggregateMarketValue')
        units_outstanding = child_text(tag, 'noOfUnitsOutstanding')
        approx_sale_date = child_text(tag, 'approxSaleDate')
        exchange_name = child_text(tag, 'securitiesExchangeName')

        # Get the broker or market maker
        broker_or_marketmaker_tag = tag.find('brokerOrMarketmakerDetails')
        broker_name = child_text(broker_or_marketmaker_tag, 'name')

        # Get the address
        address_el = broker_or_marketmaker_tag.find('address')
        address = Address(
            street1=child_text(address_el, 'street1'),
            street2=child_text(address_el, 'street2'),
            city=child_text(address_el, 'city'),
            state_or_country=child_text(address_el, 'stateOrCountry'),
            zipcode=child_text(address_el, 'zipCode')
        )
        return cls(
            security_class=security_class,
            units_sold=int(units_sold),
            aggregate_market_value=float(aggregate_market_value) if aggregate_market_value else None,
            units_outstanding=int(units_outstanding),
            approx_sale_date=approx_sale_date,
            exchange_name=exchange_name,
            broker_name=broker_name,
            broker_address=address
        )


@dataclass(frozen=True)
class SecuritiesToBeSold:
    """
          <securitiesToBeSold>
         <securitiesClassTitle>Common stock - 2</securitiesClassTitle>
         <acquiredDate>01/01/1933</acquiredDate>
         <natureOfAcquisitionTransaction>Employee Stock Award -1</natureOfAcquisitionTransaction>
         <nameOfPersonfromWhomAcquired>Issuer-1</nameOfPersonfromWhomAcquired>
         <isGiftTransaction>Y</isGiftTransaction>
         <donarAcquiredDate>01/01/1933</donarAcquiredDate>
         <amountOfSecuritiesAcquired>17087</amountOfSecuritiesAcquired>
         <paymentDate>08/15/2021</paymentDate>
         <natureOfPayment>CASH-25</natureOfPayment>
      </securitiesToBeSold>
    """
    security_class: str
    acquired_date: str
    nature_of_acquisition_transaction: str
    name_of_person_from_whom_acquired: str
    is_gift_transaction: str
    donar_acquired_date: str
    amount_of_securities_acquired: int
    payment_date: str
    nature_of_payment: str

    def to_dict(self):
        # Convert this object to a dictionary
        return {
            'security_class': self.security_class,
            'acquired_date': self.acquired_date,
            'nature_of_acquisition': self.nature_of_acquisition_transaction,
            'acquired_from': self.name_of_person_from_whom_acquired,
            'is_gift': self.is_gift_transaction,
            'donar_acquired_date': self.donar_acquired_date,
            'amount_acquired': self.amount_of_securities_acquired,
            'payment_date': self.payment_date,
            'nature_of_payment': self.nature_of_payment
        }

    @classmethod
    def from_tag(cls, tag: Tag):
        security_class = child_text(tag, 'securitiesClassTitle')
        acquired_date = child_text(tag, 'acquiredDate')
        nature_of_acquisition_transaction = child_text(tag, 'natureOfAcquisitionTransaction')
        name_of_person_from_whom_acquired = child_text(tag, 'nameOfPersonfromWhomAcquired')
        is_gift_transaction = child_text(tag, 'isGiftTransaction')
        donar_acquired_date = child_text(tag, 'donarAcquiredDate')
        amount_of_securities_acquired = child_text(tag, 'amountOfSecuritiesAcquired')
        payment_date = child_text(tag, 'paymentDate')
        nature_of_payment = child_text(tag, 'natureOfPayment')
        return cls(
            security_class=security_class,
            acquired_date=acquired_date,
            nature_of_acquisition_transaction=nature_of_acquisition_transaction,
            name_of_person_from_whom_acquired=name_of_person_from_whom_acquired,
            is_gift_transaction=is_gift_transaction,
            donar_acquired_date=donar_acquired_date,
            amount_of_securities_acquired=int(amount_of_securities_acquired),
            payment_date=payment_date,
            nature_of_payment=nature_of_payment
        )


@dataclass(frozen=True)
class SecuritiesSoldPast3Months:
    """
          <securitiesSoldInPast3Months>
         <sellerDetails>
            <name>Virtu Financial</name>
            <address>
               <com:street1>One Liberty Plaza</com:street1>
               <com:street2>165 Broadway</com:street2>
               <com:city>New York</com:city>
               <com:stateOrCountry>NY</com:stateOrCountry>
               <com:zipCode>10006</com:zipCode>
            </address>
         </sellerDetails>
         <securitiesClassTitle>Common Stock</securitiesClassTitle>
         <saleDate>08/27/2022</saleDate>
         <amountOfSecuritiesSold>0</amountOfSecuritiesSold>
         <grossProceeds>0.00</grossProceeds>
      </securitiesSoldInPast3Months>
    """
    seller_name: str
    seller_address: Address
    security_class: str
    sale_date: str
    amount_of_securities_sold: int
    gross_proceeds: float

    def to_dict(self):
        # Convert this object to a dictionary
        return {
            'security_class': self.security_class,
            'seller_name': self.seller_name,
            'sale_date': self.sale_date,
            'amount_sold': self.amount_of_securities_sold,
            'gross_proceeds': self.gross_proceeds
        }

    @classmethod
    def from_tag(cls, tag: Tag):
        seller_details = tag.find('sellerDetails')
        seller_name = child_text(seller_details, 'name')
        # Get the address
        address_el = seller_details.find('address')
        seller_address = Address(
            street1=child_text(address_el, 'street1'),
            street2=child_text(address_el, 'street2'),
            city=child_text(address_el, 'city'),
            state_or_country=child_text(address_el, 'stateOrCountry'),
            zipcode=child_text(address_el, 'zipCode')
        )
        security_class = child_text(tag, 'securitiesClassTitle')
        sale_date = child_text(tag, 'saleDate')
        amount_of_securities_sold = child_text(tag, 'amountOfSecuritiesSold')
        gross_proceeds = child_text(tag, 'grossProceeds')
        return cls(
            seller_name=seller_name,
            seller_address=seller_address,
            security_class=security_class,
            sale_date=sale_date,
            amount_of_securities_sold=int(amount_of_securities_sold),
            gross_proceeds=float(gross_proceeds) if gross_proceeds else None
        )


@dataclass(frozen=True)
class NoticeSignature:
    """
          <noticeSignature>
         <noticeDate>09/08/2022</noticeDate>
         <planAdoptionDates>
            <planAdoptionDate>08/15/2022</planAdoptionDate>
            <planAdoptionDate>08/15/2022</planAdoptionDate>
            <planAdoptionDate>01/02/1933</planAdoptionDate>
         </planAdoptionDates>
         <signature>/s/ Jan van der Velden</signature>
      </noticeSignature>
    """
    notice_date: str
    plan_adoption_dates: List[str]
    signature: str

    @classmethod
    def from_tag(cls, tag: Tag):
        notice_date = child_text(tag, 'noticeDate')
        plan_adoption_dates = [child_text(d, 'planAdoptionDate') for d in tag.find_all('planAdoptionDate')]
        signature = child_text(tag, 'signature')
        return cls(
            notice_date=notice_date,
            plan_adoption_dates=plan_adoption_dates,
            signature=signature
        )


class Form144:

    def __init__(self,
                 filing,
                 filer: Filer,
                 contact:Contact,
                 issuer_cik:str,
                 issuer_name:str,
                 sec_file_number:str,
                 issuer_contact_phone:str,
                 person_selling:str,
                 relationships:List[str],
                 address:Address,
                 securities_information:pd.DataFrame,
                 securities_to_be_sold:List[SecuritiesToBeSold],
                 securities_sold_past_3_months: List[SecuritiesSoldPast3Months],
                 nothing_to_report:bool,
                 remarks:str,
                 notice_signature:NoticeSignature
                 ):
        assert filing.form in ['144', '144/A'], f"This form should be a Form 144 but was {filing.form}"
        self._filing = filing
        self.filer = filer
        self.contact:Contact = contact
        self.issuer_cik = issuer_cik
        self.issuer_name = issuer_name
        self.sec_file_number = sec_file_number
        self.issuer_contact_phone = issuer_contact_phone
        self.person_selling = person_selling
        self.relationships = relationships
        self.address = address
        self.securities_information:pd.DataFrame = securities_information
        self.securities_to_be_sold = securities_to_be_sold
        self.securities_sold_past_3_months = securities_sold_past_3_months
        self.nothing_to_report = nothing_to_report
        self.remarks = remarks
        self.notice_signature = notice_signature

    def data(self):
        return pd.DataFrame(
            [{'issuer_cik':self.issuer_cik,
              'issuer_name':self.issuer_name,
              'sec_file_number':self.sec_file_number,
              }]
        )

    @staticmethod
    def parse_xml(xml: str) -> Dict[str, object]:
        soup = BeautifulSoup(xml, 'xml')

        root = soup.find('edgarSubmission')

        form144 = {}

        header_data = root.find('headerData')
        filer_info_el = header_data.find('filerInfo')

        filer_el = filer_info_el.find('filer')
        filer_credentials_el = filer_el.find('filerCredentials')
        form144['filer'] = Filer(
            cik=child_text(filer_credentials_el, 'cik'),
            entity_name=child_text(filer_credentials_el, 'name'),
            file_number=child_text(filer_credentials_el, 'secFileNumber')
        )

        # Contact info
        contact_el = filer_el.find('contact')
        form144['contact'] = Contact(
                name=child_text(contact_el, 'name'),
                phone_number=child_text(contact_el, 'phone'),
                email=child_text(contact_el, 'email')
            ) if contact_el else None

        form_data = root.find('formData')
        # Issuer
        issuer_el = form_data.find('issuerInfo')
        form144['issuer_cik'] = child_text(issuer_el, 'issuerCik')
        form144['issuer_name'] = child_text(issuer_el, 'issuerName')
        form144['sec_file_number'] = child_text(issuer_el, 'secFileNumber')
        form144['issuer_contact_phone'] = child_text(issuer_el, 'issuerContactPhone')
        form144['person_selling'] = child_text(issuer_el, 'nameOfPersonForWhoseAccountTheSecuritiesAreToBeSold')

        relationship_el = issuer_el.find('relationshipsToIssuer')
        form144['relationships'] = child_values(relationship_el, 'relationshipToIssuer')

        issuer_address_el = issuer_el.find("issuerAddress")
        address: Address = Address(
            street1=child_text(issuer_address_el, "street1"),
            street2=child_text(issuer_address_el, "street2"),
            city=child_text(issuer_address_el, "city"),
            state_or_country=child_text(issuer_address_el, "stateOrCountry"),
            state_or_country_description=child_text(issuer_address_el, "stateOrCountryDescription"),
            zipcode=child_text(issuer_address_el, "zipCode")
        )
        form144['address'] = address

        # Securities Information
        form144['securities_information'] = pd.DataFrame([
            SecuritiesInformation.from_tag(el).to_dict()
            for el in form_data.find_all('securitiesInformation')
        ])

        # Securities to be sold
        form144['securities_to_be_sold'] = pd.DataFrame([
            SecuritiesToBeSold.from_tag(el).to_dict()
            for el in form_data.find_all('securitiesToBeSold')
        ])
        # Nothing to report flag
        form144['nothing_to_report'] = child_text(form_data, 'nothingToReportFlagOnSecuritiesSoldInPast3Months')

        # Securities sold in past 3 months
        form144['securities_sold_past_3_months'] = pd.DataFrame([
            SecuritiesSoldPast3Months.from_tag(el).to_dict()
            for el in form_data.find_all('securitiesSoldInPast3Months')
        ])

        # Remarks
        form144['remarks'] = child_text(form_data, 'remarks')

        # Notice signature
        form144['notice_signature'] = NoticeSignature.from_tag(form_data.find('noticeSignature'))
        return form144

    @classmethod
    def from_filing(cls, filing):
        assert filing.form in ['144', '144/A'], f"This form should be a Form 144 but was {filing.form}"
        xml = filing.xml()

        form144 = cls.parse_xml(xml)
        return cls(filing=filing, **form144)

    def __rich__(self):
        contact_table = Table("Name", "Phone", "Email", box=box.SIMPLE)
        contact_table.add_row(self.contact.name if self.contact else "-",
                              self.contact.phone_number if self.contact else "-",
                              self.contact.email if self.contact else "-")


        # Securities Information Table
        securities_information_table = Table("Security Class", "Sold", "Remaining", "Value",
                                             "Sale Date", "Exchange", "Broker",
                                             box=box.SIMPLE, title="Securities Information")
        for row in self.securities_information.itertuples():
            securities_information_table.add_row(row.security_class,
                                                 str(row.units_sold),
                                                 str(row.units_outstanding),
                                                 str(row.market_value),
                                                 row.approx_sale_date,
                                                 row.exchange_name,
                                                 row.broker_name)

        # Securities to be sold
        securities_to_be_sold_table = Table("Security Class", "Date Acquired", "Nature of acquistion",
                                            "Acquired From", "Gift", "Amount Acquired", "Payment Date",
                                            "Nature of Payment", box=box.SIMPLE, title="Securities to be sold")
        for row in self.securities_to_be_sold.itertuples():
            securities_to_be_sold_table.add_row(row.security_class,
                                                row.acquired_date,
                                                row.nature_of_acquisition,
                                                row.acquired_from,
                                                row.is_gift,
                                                str(row.amount_acquired),
                                                row.payment_date,
                                                row.nature_of_payment)

        # Securities sold in past 3 months
        securities_sold_past_3_months_table = Table("Security Class", "Sale Date", "Amount Sold",
                                                    "Proceeds", "Seller Name", box=box.SIMPLE,
                                                    title="Securities sold in past 3 months")
        for row in self.securities_sold_past_3_months.itertuples():
            securities_sold_past_3_months_table.add_row(row.security_class,
                                                row.seller_name,
                                                str(row.amount_of_securities_sold),
                                                str(row.gross_proceeds),
                                                row.seller_name)

        # Notice signature
        notice_signature_table = Table("Signature", "Date", box=box.SIMPLE, title="Notice Signature")
        notice_signature_table.add_row(self.notice_signature.signature, self.notice_signature.notice_date)

        # Plan adoption dates
        plan_adoption_dates_table = Table("Date", box=box.SIMPLE, title="Plan Adoption Dates")
        if len(self.notice_signature.plan_adoption_dates) == 0:
            plan_adoption_dates_table.add_row(" "*20)
        else:
            for date in self.notice_signature.plan_adoption_dates:
                plan_adoption_dates_table.add_row(date)
        return Panel(
            Group(
                self._filing.__rich__(),
                contact_table,
                securities_information_table,
                securities_to_be_sold_table,
                securities_sold_past_3_months_table,
                Columns([notice_signature_table, plan_adoption_dates_table])
            )
        )

    def __repr__(self):
        return repr_rich(self.__rich__())