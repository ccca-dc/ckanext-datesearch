import logging

import ckan.plugins as plugins
import ckan.plugins.toolkit as toolkit
from datetime import datetime

log = logging.getLogger(__name__)


class DateSearchPlugin(plugins.SingletonPlugin):
    plugins.implements(plugins.IConfigurer)
    plugins.implements(plugins.IPackageController, inherit=True)

    def update_config(self, config):
        toolkit.add_template_directory(config, 'templates')
        toolkit.add_resource('fanstatic', 'ckanext-datesearch')

    def before_search(self, search_params):
        extras = search_params.get('extras')
        if not extras:
            # There are no extras in the search params, so do nothing.
            return search_params

        start_date = extras.get('ext_startdate')

        end_date = extras.get('ext_enddate')
        if not start_date and not end_date:
            # The user didn't select either a start and/or end date, so do nothing.
            return search_params
        if not start_date:
            start_date = '*'
        if not end_date:
            print ("not end")
            end_date = '*'

        zerodate = datetime.strptime("0001-01-01T00:00:00", '%Y-%m-%dT%H:%M:%S')
        finaldate = datetime.strptime("9999-01-01T00:00:00", '%Y-%m-%dT%H:%M:%S')
        zerodate = "0000-00-01T00:00:00Z"
        finaldate = "9999-99-99T00:00:00Z"
        # Add a date-range query with the selected start and/or end dates into the Solr facet queries.
        fq = search_params.get('fq', '')
        #fq = '{fq} +extras_PublicationTimestamp:[{sd} TO {ed}]'.format(fq=fq, sd=start_date, ed=end_date)
        print ("**************ANJA datesearch")
        print (fq)
        #fq = '{fq} +(extras_iso_exTempStart:[{zd} TO {sd}] AND  extras_iso_exTempEnd:[{ed} TO {fd}])'.format(fq=fq, sd=str(start_date), ed=str(end_date), zd=str(zerodate), fd=str(finaldate))
        fq = '{fq} +(extras_iso_exTempStart:["{zd}" TO "{sd}"] AND  extras_iso_exTempEnd:["{ed}" TO "{fd}"])'.format(fq=fq, sd=str(start_date), ed=str(end_date), zd=str(zerodate), fd=str(finaldate))


        search_params['fq'] = fq

        # Just for printing -Anja
        if not start_date:
            start_date = "empty"
        if not end_date:
            end_date = "empty"
        print ("startdate: " + start_date)
        print ("enddate: " + end_date)

        return search_params
