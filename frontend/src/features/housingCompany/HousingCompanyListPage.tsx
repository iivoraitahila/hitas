import {useState} from "react";

import {Button, IconPlus, IconSearch} from "hds-react";
import {Link} from "react-router-dom";

import {useGetDevelopersQuery, useGetHousingCompaniesQuery, useGetPropertyManagersQuery} from "../../app/services";
import {
    FilterIntegerField,
    FilterTextInputField,
    Heading,
    ListPageNumbers,
    QueryStateHandler,
} from "../../common/components";
import FilterRelatedModelComboboxField from "../../common/components/FilterRelatedModelComboboxField";
import {IHousingCompany, IHousingCompanyListResponse} from "../../common/schemas";
import {formatDate} from "../../common/utils";

const HousingCompanyListItem = ({id, name, address, date}): JSX.Element => {
    return (
        <Link to={`/housing-companies/${id}`}>
            <li className="results-list__item">
                <div className="name">{name}</div>
                <div className="address">
                    {address.street_address}
                    <br />
                    {address.postal_code}, {address.city}
                </div>
                <div className="date">{formatDate(date)}</div>
            </li>
        </Link>
    );
};

const HousingCompanyResultsList = ({filterParams}): JSX.Element => {
    const [currentPage, setCurrentPage] = useState(1);
    const {data, error, isLoading} = useGetHousingCompaniesQuery({...filterParams, page: currentPage});

    const LoadedHousingCompanyResultsList = ({data}: {data: IHousingCompanyListResponse}) => {
        return (
            <>
                <div className="list-amount">
                    Haun tulokset: {data.page.total_items} {data.page.total_items > 1 ? "yhtiötä" : "yhtiö"}
                </div>
                <div className="list-headers">
                    <div className="list-header name">Yhtiö</div>
                    <div className="list-header address">Osoite</div>
                    <div className="list-header date">Valmistunut</div>
                </div>
                <ul className="results-list">
                    {data.contents.map((item: IHousingCompany) => (
                        <HousingCompanyListItem
                            key={item.id}
                            id={item.id}
                            name={item.name}
                            address={item.address}
                            date={item.date}
                        />
                    ))}
                </ul>
            </>
        );
    };

    return (
        <div className="results">
            <QueryStateHandler
                data={data}
                error={error}
                isLoading={isLoading}
            >
                <LoadedHousingCompanyResultsList data={data as IHousingCompanyListResponse} />
                <ListPageNumbers
                    currentPage={currentPage}
                    setCurrentPage={setCurrentPage}
                    pageInfo={(data as IHousingCompanyListResponse)?.page}
                />
            </QueryStateHandler>
        </div>
    );
};

const HousingCompanyFilters = ({filterParams, setFilterParams}): JSX.Element => {
    return (
        <div className="filters">
            <FilterTextInputField
                label="Osoite"
                filterFieldName="street_address"
                filterParams={filterParams}
                setFilterParams={setFilterParams}
            />
            <FilterIntegerField
                label="Postinumero"
                minLength={5}
                maxLength={5}
                filterFieldName="postal_code"
                filterParams={filterParams}
                setFilterParams={setFilterParams}
            />
            <FilterRelatedModelComboboxField
                label="Rakennuttaja"
                queryFunction={useGetDevelopersQuery}
                labelField="value"
                filterFieldName="developer"
                filterParams={filterParams}
                setFilterParams={setFilterParams}
            />
            <FilterRelatedModelComboboxField
                label="Isännöitsijä"
                queryFunction={useGetPropertyManagersQuery}
                labelField="name"
                filterFieldName="property_manager"
                filterParams={filterParams}
                setFilterParams={setFilterParams}
            />
            <FilterIntegerField
                label="Yhtiön arkistotunnus"
                minLength={1}
                maxLength={10}
                filterFieldName="archive_id"
                filterParams={filterParams}
                setFilterParams={setFilterParams}
            />
        </div>
    );
};

const HousingCompanyListPage = (): JSX.Element => {
    const [filterParams, setFilterParams] = useState({});

    return (
        <div className="view--housing-company-list">
            <Heading>
                <span>Kaikki kohteet</span>
                <Link to="create">
                    <Button
                        theme="black"
                        iconLeft={<IconPlus />}
                    >
                        Lisää uusi yhtiö
                    </Button>
                </Link>
            </Heading>
            <div className="listing">
                <div className="search">
                    <FilterTextInputField
                        label=""
                        filterFieldName="display_name"
                        filterParams={filterParams}
                        setFilterParams={setFilterParams}
                    />
                    <IconSearch />
                </div>
                <HousingCompanyResultsList filterParams={filterParams} />
                <HousingCompanyFilters
                    filterParams={filterParams}
                    setFilterParams={setFilterParams}
                />
            </div>
        </div>
    );
};

export default HousingCompanyListPage;
