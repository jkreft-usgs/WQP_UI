import queryService from '../queryService';
import { getQueryString, buildCurlString } from '../utils';

/*
 * Initializes the windows which show the various API calls
 * @param {Object} options
 *      @prop {Jquery element} $container - The container containing the show button and the query windows.
 *      @prop {Function} getQueryParamArray - Returns the current query parameter array
 *      @prop {Function} getResultType - Returns the result type value the user selected in the form
 *      @returns {Array of Objects with name and value properties}
 */
export default class ShowAPIView {
    constructor({$container, getQueryParamArray, getResultType}) {
        this.$container = $container;
        this.getQueryParamArray = getQueryParamArray;
        this.getResultType = getResultType;
    }

    initialize() {
        let $apiQueryDiv = this.$container.find('#api-queries-div');
        let $apiQueryTitle = this.$container.find('#query-div b');
        let $apiQueryText = this.$container.find('#query-div textarea');
        let $cUrlText = this.$container.find('#curl-query-div textarea');
        let $wfsText = this.$container.find('#getfeature-query-div textarea');

        this.$container.find('#show-queries-button').click(() => {
            let resultType = this.getResultType();
            let queryParamArray = this.getQueryParamArray();
console.log('queryParamArray ' + JSON.stringify(queryParamArray));
            let queryWithoutDataProfileArray = queryParamArray.filter((param) => {
               return param.name !== 'dataProfile';
            });
console.log('queryWithoutDataProfileArray ' + JSON.stringify(queryWithoutDataProfileArray))

            let queryString = getQueryString(queryParamArray);
            let queryStringWithoutDataProfile = getQueryString(queryWithoutDataProfileArray);
            let apiQueryString =  '';

            if (dataProfileUsed[resultType]) {
                apiQueryString = queryService.getFormUrl(resultType, queryString);
            } else {
                apiQueryString = queryService.getFormUrl(resultType, queryStringWithoutDataProfile);
            }

            let curlString = buildCurlString(resultType, queryParamArray);

            $apiQueryDiv.show();
            $apiQueryTitle.html(resultType.replace(/([A-Z])/g, ' $1'));
            $apiQueryText.html(apiQueryString);
            $cUrlText.html(curlString);
            $wfsText.html(L.WQPSitesLayer.getWfsGetFeatureUrl(queryWithoutDataProfileArray));
        });
    }
}

export const dataProfileUsed = {
    'Station': false,
    'Project': false,
    'ProjectMonitoringLocationWeighting': false,
    'Result': true,
    'Activity': false,
    'ActivityMetric': false,
    'ResultDetectionQuantitationLimit': false,
    'default': false
};
