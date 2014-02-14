
import unittest

from freezegun import freeze_time
from datetime import date

from collector.trending \
    import parse_query, get_date, sum_data, assign_day_to_week


class test_sum_metrics(unittest.TestCase):
    @freeze_time("2014-02-12 01:00:00")
    def test_sum_by_day(self):
        dates = get_date()
        data = [{'metrics': {u'pageviews': u'03'},
                 'dimensions': {u'pagePath': u'/foo',
                                u'pageTitle': u'foo',
                                u'day': u'29',
                                u'month': u'01',
                                u'year': u'2014'}},
                {'metrics': {u'pageviews': u'10'},
                 'dimensions': {u'pagePath': u'/foo',
                                u'pageTitle': u'foo',
                                u'day': u'05',
                                u'month': u'02',
                                u'year': u'2014'}},
                {'metrics': {u'pageviews': u'07'},
                 'dimensions': {u'pagePath': u'/bar',
                                u'pageTitle': u'bar',
                                u'day': u'04',
                                u'month': u'02',
                                u'year': u'2014'}},
                {'metrics': {u'pageviews': u'23'},
                 'dimensions': {u'pagePath': u'/bar',
                                u'pageTitle': u'bar',
                                u'day': u'11',
                                u'month': u'02',
                                u'year': u'2014'}}]

        collapsed_data = sum_data(data, 'pageviews', 'pagePath', dates)

        self.assertEqual(len(collapsed_data), 2)
        self.assertEqual(collapsed_data['/foo'], {u'pageTitle': u'foo',
                                                  'week1': 3, 'week2': 10})
        self.assertEqual(collapsed_data['/bar'], {u'pageTitle': u'bar',
                                                  'week1': 7, 'week2': 23})


class test_dates(unittest.TestCase):

    @freeze_time("2014-02-12 01:00:00")
    def test_assign_day_to_week(self):

        dates = get_date()

        self.assertEqual(assign_day_to_week('29', '01', '2014', dates), 1)
        self.assertEqual(assign_day_to_week('04', '02', '2014', dates), 1)
        self.assertEqual(assign_day_to_week('05', '02', '2014', dates), 2)
        self.assertEqual(assign_day_to_week('11', '02', '2014', dates), 2)

    @freeze_time("2013-01-05 01:00:00")
    def test_assign_day_to_week_across_year_boundaries(self):

        dates = get_date()

        self.assertEqual(assign_day_to_week('22', '12', '2012', dates), 1)
        self.assertEqual(assign_day_to_week('28', '12', '2012', dates), 1)
        self.assertEqual(assign_day_to_week('29', '12', '2012', dates), 2)
        self.assertEqual(assign_day_to_week('04', '01', '2013', dates), 2)


class test_query_parsing(unittest.TestCase):
    def test_query_parsing_when_no_metric(self):
        query = {}
        self.assertRaises(
            Exception,
            parse_query, query
        )

    def test_query_parsing_when_empty_metric(self):
        query = {'metric': ''}
        self.assertRaises(
            Exception,
            parse_query, query
        )

    def test_when_just_a_metric(self):
        query = {'metric': 'pageview'}
        parsed_query = parse_query(query)

        self.assertEquals(
            parsed_query['dimensions'],
            ['day', 'month', 'year']
        )

    def test_when_a_metric_and_dimensions(self):
        query = {
            'metric': 'pageview',
            'dimensions': ['pageTitle', 'pagePath']
        }
        parsed_query = parse_query(query)

        self.assertEquals(
            parsed_query['dimensions'],
            ['pageTitle', 'pagePath', 'day', 'month', 'year']
        )


class test_date_picking(unittest.TestCase):

    @freeze_time("2014-02-12 01:00:00")
    def test_returns_last_two_weeks(self):
        (start, middle, end) = get_date()

        self.assertEqual(
            end,
            date(2014, 02, 11)
        )
        self.assertEqual(
            middle,
            date(2014, 02, 05)
        )
        self.assertEqual(
            start,
            date(2014, 01, 29)
        )
