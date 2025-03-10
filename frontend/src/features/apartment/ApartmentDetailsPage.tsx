import {useState} from "react";

import {Button, Card, Dialog, IconDownload, IconGlyphEuro, IconLock, IconLockOpen, Tabs} from "hds-react";
import {Link, useParams} from "react-router-dom";

import {
    downloadApartmentMaximumPricePDF,
    downloadApartmentUnconfirmedMaximumPricePDF,
    useGetApartmentDetailQuery,
    useGetHousingCompanyDetailQuery,
} from "../../app/services";
import {DetailField, ImprovementsTable, QueryStateHandler} from "../../common/components";
import FormTextInputField from "../../common/components/formInputField/FormTextInputField";
import {
    IApartmentConditionOfSale,
    IApartmentConfirmedMaximumPrice,
    IApartmentDetails,
    IApartmentUnconfirmedMaximumPrice,
    IHousingCompanyDetails,
    IOwnership,
} from "../../common/schemas";
import {formatAddress, formatDate, formatMoney} from "../../common/utils";
import ApartmentHeader from "./components/ApartmentHeader";

const SingleApartmentConditionOfSale = ({conditionsOfSale}: {conditionsOfSale: IApartmentConditionOfSale[]}) => {
    return (
        <li>
            <h3>
                {conditionsOfSale[0].owner.name} ({conditionsOfSale[0].owner.identifier})
            </h3>
            <ul>
                {conditionsOfSale.map((cos) => (
                    <li
                        key={cos.id}
                        className={cos.fulfilled ? "resolved" : "unresolved"}
                    >
                        <Link
                            to={`/housing-companies/${cos.apartment.housing_company.id}/apartments/${cos.apartment.id}`}
                        >
                            {cos.fulfilled ? <IconLockOpen /> : <IconLock />}
                            {formatAddress(cos.apartment.address)}
                        </Link>
                    </li>
                ))}
            </ul>
        </li>
    );
};

const ApartmentConditionsOfSaleCard = ({apartment}: {apartment: IApartmentDetails}) => {
    const conditionsOfSale = apartment.conditions_of_sale;
    // Create a dict with owner id as key, and all of their conditions of sale in a list as value
    interface IGroupedConditionsOfSale {
        [ownerId: string]: IApartmentConditionOfSale[];
    }
    const groupedConditionsOfSale: IGroupedConditionsOfSale = conditionsOfSale.reduce((acc, obj) => {
        if (obj.owner.id in acc) {
            acc[obj.owner.id].push(obj);
        } else {
            acc[obj.owner.id] = [obj];
        }
        return acc;
    }, {});

    return (
        <Card>
            <div className="row row--buttons">
                <Link to="sales">
                    <Button
                        theme="black"
                        iconLeft={<IconGlyphEuro />}
                    >
                        Kauppatapahtuma
                    </Button>
                </Link>
                <Link to="conditions-of-sale">
                    <Button
                        theme="black"
                        iconLeft={<IconLock />}
                    >
                        Muokkaa myyntiehtoja
                    </Button>
                </Link>
            </div>
            <label className="card-heading">
                <IconLock /> Myyntiehdot
            </label>
            {Object.keys(groupedConditionsOfSale).length ? (
                <ul>
                    {Object.entries(groupedConditionsOfSale).map(([ownerId, cos]) => (
                        <SingleApartmentConditionOfSale
                            key={ownerId}
                            conditionsOfSale={cos}
                        />
                    ))}
                </ul>
            ) : (
                <span>Ei myyntiehtoja.</span>
            )}
        </Card>
    );
};

interface UnconfirmedPriceRowProps {
    label: string;
    unconfirmedPrice: IApartmentUnconfirmedMaximumPrice;
}
const UnconfirmedPriceRow = ({label, unconfirmedPrice}: UnconfirmedPriceRowProps) => {
    return (
        <div className={`price${unconfirmedPrice.maximum ? " price--current-top" : ""}`}>
            <span className="basis">{label}</span>
            <span className="amount">
                <span className="value">{formatMoney(unconfirmedPrice.value)}</span>
            </span>
        </div>
    );
};

const ConfirmedPriceDetails = ({confirmed}: {confirmed: IApartmentConfirmedMaximumPrice}) => {
    if (confirmed === null) return <p className="confirmed-price">-</p>;
    return (
        <>
            <div className="confirmed-price">{formatMoney(confirmed.maximum_price)}</div>
            <div className="confirmed-price__date">Vahvistettu: {formatDate(confirmed.confirmed_at.split("T")[0])}</div>
            <div className="confirmed-price__date">
                Voimassa:{" "}
                {new Date() <= new Date(confirmed.valid.valid_until) ? (
                    `${formatDate(confirmed.valid.valid_until)} asti`
                ) : (
                    <span>
                        <span className="invalid">{formatDate(confirmed.valid.valid_until)} - ei voimassa</span>
                    </span>
                )}
            </div>
        </>
    );
};

interface UnconfirmedPricesDownloadModalProps {
    apartment: IApartmentDetails;
    isVisible: boolean;
    setIsVisible;
}
const UnconfirmedPricesDownloadModal = ({apartment, isVisible, setIsVisible}: UnconfirmedPricesDownloadModalProps) => {
    const [additionalInfo, setAdditionalInfo] = useState("");

    return (
        <Dialog
            id="unconfirmed-prices-download-modal"
            closeButtonLabelText=""
            aria-labelledby=""
            isOpen={isVisible}
            close={() => setIsVisible(false)}
            boxShadow
        >
            <Dialog.Header
                id="unconfirmed-prices-download-modal__header"
                title="Lataa Enimmäishinta-arvio"
            />
            <Dialog.Content>
                <FormTextInputField
                    id="input-additional_details"
                    key="input-additional_details"
                    label="Lisätietoja"
                    size="large"
                    value={additionalInfo}
                    setFieldValue={setAdditionalInfo}
                    tooltipText="Lisätietokenttään kirjoitetaan, jos laskelmassa on jotain erityistä, mitä osakkaan on syytä tietää. Kentän teksti lisätään tulostettavaan hinta-arvio PDF:ään."
                />
            </Dialog.Content>
            <Dialog.ActionButtons>
                <Button
                    onClick={() => setIsVisible(false)}
                    variant="secondary"
                    theme="black"
                    size="small"
                >
                    Sulje
                </Button>
                <Button
                    theme="black"
                    size="small"
                    iconLeft={<IconDownload />}
                    onClick={() => downloadApartmentUnconfirmedMaximumPricePDF(apartment, additionalInfo)}
                >
                    Lataa Hinta-arvio
                </Button>
            </Dialog.ActionButtons>
        </Dialog>
    );
};

const ApartmentMaximumPricesCard = ({apartment}: {apartment: IApartmentDetails}) => {
    const isPre2011 = apartment.prices.maximum_prices.unconfirmed.pre_2011 !== null;
    const unconfirmedPrices = isPre2011
        ? apartment.prices.maximum_prices.unconfirmed.pre_2011
        : apartment.prices.maximum_prices.unconfirmed.onwards_2011;
    const [isUnconfirmedMaximumPriceModalVisible, setIsUnconfirmedMaximumPriceModalVisible] = useState(false);

    return (
        <Card>
            <label className="card-heading">Vahvistamaton enimmäishinta</label>
            <div className="unconfirmed-prices">
                <UnconfirmedPriceRow
                    label="Markkinahintaindeksi"
                    unconfirmedPrice={unconfirmedPrices.market_price_index}
                />
                <UnconfirmedPriceRow
                    label="Rakennuskustannusindeksi"
                    unconfirmedPrice={unconfirmedPrices.construction_price_index}
                />
                <UnconfirmedPriceRow
                    label="Rajaneliöhinta"
                    unconfirmedPrice={unconfirmedPrices.surface_area_price_ceiling}
                />
                <div className="align-content-right">
                    <Button
                        theme="black"
                        size="small"
                        variant="secondary"
                        onClick={() => setIsUnconfirmedMaximumPriceModalVisible(true)}
                        disabled={
                            // Button should be disabled if any of the price calculations are missing
                            !(
                                unconfirmedPrices.market_price_index.value &&
                                unconfirmedPrices.construction_price_index.value &&
                                unconfirmedPrices.surface_area_price_ceiling.value
                            )
                        }
                    >
                        Lataa Hinta-arvio
                    </Button>
                </div>
            </div>

            <label className="card-heading">Vahvistettu enimmäishinta</label>
            <ConfirmedPriceDetails confirmed={apartment.prices.maximum_prices.confirmed} />
            <div className="align-content-right">
                <Button
                    theme="black"
                    size="small"
                    variant="secondary"
                    iconLeft={<IconDownload />}
                    onClick={() => downloadApartmentMaximumPricePDF(apartment)}
                    disabled={
                        !apartment.prices.maximum_prices.confirmed || !apartment.prices.maximum_prices.confirmed.id
                    }
                >
                    Lataa enimmäishintalaskelma
                </Button>
                <Link to="max-price">
                    <Button
                        theme="black"
                        size="small"
                        disabled={!apartment.completion_date}
                    >
                        Vahvista
                    </Button>
                </Link>
            </div>

            <UnconfirmedPricesDownloadModal
                apartment={apartment}
                isVisible={isUnconfirmedMaximumPriceModalVisible}
                setIsVisible={setIsUnconfirmedMaximumPriceModalVisible}
            />
        </Card>
    );
};

const LoadedApartmentDetails = ({data}: {data: IApartmentDetails}): JSX.Element => {
    const {
        data: housingCompanyData,
        error: housingCompanyError,
        isLoading: isHousingCompanyLoading,
    } = useGetHousingCompanyDetailQuery(data.links.housing_company.id);

    return (
        <>
            <ApartmentHeader
                apartment={data as IApartmentDetails}
                showEditButton={true}
            />
            <h2 className="apartment-stats">
                <span className="apartment-stats--number">
                    {data.address.stair}
                    {data.address.apartment_number}
                </span>
                <span>
                    {data.rooms || ""}
                    {data.type?.value || ""}
                </span>
                <span>{data.surface_area ? data.surface_area + "m²" : ""}</span>
                <span>{data.address.floor ? data.address.floor + ".krs" : ""}</span>
            </h2>
            <div className="apartment-action-cards">
                <ApartmentMaximumPricesCard apartment={data} />
                <ApartmentConditionsOfSaleCard apartment={data} />
            </div>
            <div className="apartment-details">
                <div className="tab-area">
                    <Tabs>
                        <Tabs.TabList className="tab-list">
                            <Tabs.Tab>Perustiedot</Tabs.Tab>
                            <Tabs.Tab>Dokumentit</Tabs.Tab>
                        </Tabs.TabList>
                        <Tabs.TabPanel>
                            <div className="company-details__tab basic-details">
                                <div className="row">
                                    <div>
                                        <DetailField
                                            label="Kauppakirjahinta"
                                            value={formatMoney(data.prices.latest_sale_purchase_price)}
                                        />
                                    </div>
                                    <div>
                                        <DetailField
                                            label="Hankinta-arvo"
                                            value={formatMoney(data.prices.first_sale_acquisition_price)}
                                        />
                                    </div>
                                    <div>
                                        <DetailField
                                            label="Valmistumispäivä"
                                            value={formatDate(data.completion_date)}
                                        />
                                    </div>
                                </div>
                                <div className="columns">
                                    <div className="column">
                                        <label className="detail-field-label">Omistajat</label>
                                        {data.ownerships.map((ownership: IOwnership) => (
                                            <DetailField
                                                key={ownership.owner.id}
                                                value={
                                                    <>
                                                        {`${ownership.owner.name} (${ownership.owner.identifier})`}
                                                        <span> {ownership.percentage}%</span>
                                                    </>
                                                }
                                                label=""
                                            />
                                        ))}
                                        <DetailField
                                            label="Isännöitsijä"
                                            value={
                                                housingCompanyData && housingCompanyData.property_manager
                                                    ? housingCompanyData.property_manager.name
                                                    : "-"
                                            }
                                        />
                                        <label className="detail-field-label">Huomioitavaa</label>
                                        <textarea
                                            value={(data.notes as string) || ""}
                                            readOnly
                                        />
                                    </div>
                                    <div className="column">
                                        <DetailField
                                            label="Osakkeiden lukumäärä"
                                            value={data.shares ? data.shares.total : 0}
                                        />
                                        {data.shares && (
                                            <DetailField
                                                label="Osakkeet"
                                                value={`${data.shares.start} - ${data.shares.end}`}
                                            />
                                        )}
                                        <DetailField
                                            label="Luovutushinta"
                                            value={formatMoney(data.prices.first_sale_purchase_price)}
                                        />
                                        <DetailField
                                            label="Ensisijaislaina"
                                            value={formatMoney(data.prices.first_sale_share_of_housing_company_loans)}
                                        />
                                        <DetailField
                                            label="Ensimmäinen ostopäivä"
                                            value={formatDate(data.prices.first_purchase_date)}
                                        />
                                        <DetailField
                                            label="Viimeisin ostopäivä"
                                            value={formatDate(data.prices.latest_purchase_date)}
                                        />
                                        <DetailField
                                            label="Rakennusaikaiset korot (6 %)"
                                            value={
                                                data.prices.construction.interest
                                                    ? formatMoney(data.prices.construction.interest.rate_6)
                                                    : 0
                                            }
                                        />
                                        <DetailField
                                            label="Rakennusaikaiset korot (14 %)"
                                            value={
                                                data.prices.construction.interest
                                                    ? formatMoney(data.prices.construction.interest.rate_14)
                                                    : 0
                                            }
                                        />
                                        <DetailField
                                            label="Rakennusaikaiset lisätyöt"
                                            value={formatMoney(data.prices.construction.additional_work)}
                                        />
                                        {data.prices.construction.loans ? (
                                            <DetailField
                                                label="Rakennusaikaiset lainat"
                                                value={formatMoney(data.prices.construction.loans)}
                                            />
                                        ) : null}
                                        {data.prices.construction.debt_free_purchase_price ? (
                                            <DetailField
                                                label="Luovutushinta (RA)"
                                                value={formatMoney(data.prices.construction.debt_free_purchase_price)}
                                            />
                                        ) : null}
                                    </div>
                                </div>
                            </div>
                        </Tabs.TabPanel>
                        <Tabs.TabPanel>
                            <div className="company-details__tab documents">Dokumentit</div>
                        </Tabs.TabPanel>
                    </Tabs>
                </div>
                <ImprovementsTable
                    data={data}
                    title="Asuntokohtaiset parannukset"
                    editableType="apartment"
                />
                <QueryStateHandler
                    data={housingCompanyData}
                    error={housingCompanyError}
                    isLoading={isHousingCompanyLoading}
                >
                    <ImprovementsTable
                        data={housingCompanyData as IHousingCompanyDetails}
                        title="Yhtiökohtaiset parannukset"
                        editableType="housingCompany"
                        editPath={`/housing-companies/${housingCompanyData?.id}/improvements`}
                    />
                </QueryStateHandler>
            </div>
        </>
    );
};

const ApartmentDetailsPage = (): JSX.Element => {
    const params = useParams();
    const {data, error, isLoading} = useGetApartmentDetailQuery({
        housingCompanyId: params.housingCompanyId as string,
        apartmentId: params.apartmentId as string,
    });

    return (
        <div className="view--apartment-details">
            <QueryStateHandler
                data={data}
                error={error}
                isLoading={isLoading}
            >
                <LoadedApartmentDetails data={data as IApartmentDetails} />
            </QueryStateHandler>
        </div>
    );
};

export default ApartmentDetailsPage;
