import appdaemon.plugins.hass.hassapi as hass
import math
import hdate
from hdate import Location
import hdate.common
import hdate.htables
import hdate.converters
import datetime

class Molad(hass.Hass):

    def initialize(self):
        self.refresh_molad();
        self.run_hourly(self.refresh_molad_task, datetime.time(0, 0, 0));

    def sumup(self, multipliers): # event handler for any one of the multipliers
        shifts = [[2,5,204],[2,16,595],[4,8,876],[5,21,589],[1,12,793]];
        mults=[];
        mults.append(multipliers);
        out00 = self.multiply_matrix(mults,shifts); # --> 1x3 triplet
        out0 = out00[0];
        # now need to reduce by carrying
        out1 = self.carry_and_reduce(out0);
        out2 = self.convert_to_english(out1); # convert to English date/time
        return out2;

    def multiply_matrix(self,matrix1,matrix2):    
        res = [[0 for x in range(5)] for y in range(5)]
        
        for i in range(len(matrix1)):
            for j in range(len(matrix2[0])):
                for k in range(len(matrix2)):
        
                    # resulted matrix
                    res[i][j] += matrix1[i][k] * matrix2[k][j]
    
        return res;

    def carry_and_reduce(self, out0): # carry properly triple for the molad calculations
        # 7 days/week, 24 hours/day, 1080 chalakim/hours/day
        # we don't have to worry about the weeks.
        xx = out0[2]
        yy = xx%1080
        zz = math.floor(xx/1080); # chalakim
        if (yy<0):
            yy=yy+1080;
            z=zz-1; # carry up
            
        out1=[0,0,0];
        out1[2] = yy;
        xx = out0[1] + zz
        yy = xx%24
        zz = math.floor(xx/24); # hours
        if (yy<0):
            yy=yy+24;
            zz=zz-1;
            
        out1[1] = yy;
        xx = out0[0] + zz
        yy = (xx+6)%7 + 1
        zz = math.floor(xx/7); # days removing weeks - keep Shabbos=7
        if (yy<0):
            yy=yy+7;
        out1[0] = yy;
        return out1;


    def convert_to_english(self, out1): # convert triple to English time
        days = ["Sunday","Monday","Tuesday","Wednesday","Thursday","Friday","Shabbos"]
        day = out1[0];
        hours = out1[1]; # hours are measured from 6 pm of the day before
        chalakim = out1[2]; # 1080/hour, 18/minute, 3+1/3 seconds
        hours = hours-6;
        if (hours<0):
            day = day-1;
            hours = hours+24; # evening of previous day
            
        daynm = days[day-1];
        pm = "am";
        
        hournm = "morning" if (hours<12) else ("afternoon" if hours<18 else "night");
        
        if (hours>=12):
            pm = "pm";
            hours = hours-12;
            
        minutes = math.floor(chalakim/18)
        chalakim = chalakim%18; # left over
        leng = len(str(minutes))
        filler = "0" if (leng==1) else ""; # like the 0 in 3:01
        hours = 12 if (hours==0) else hours;
        out2 = str(daynm)+" "+str(hournm)+", "+str(hours)+":"+str(filler)+str(minutes)+" "+str(pm)+" and "+str(chalakim)+" chalakim";

        out = {
            "text": out2,
            "period": hournm,
            "day": daynm,
            "hours": hours,
            "minutes": minutes,
            "am/pm": pm,
            "chalakim": chalakim,
        }
        return out;

    def get_molad(self, date): # load this year into multipliers
            d = self.get_next_numeric_month_year(date);
            year = d['year']
            month = d['month']

            guachadazat = [3,6,8,11,14,17,19];
            cycles = math.floor(year/19); # 19-year cycles
            yrs = year%19; # leftover years 
            isleap = yrs in guachadazat; # is this year a leap year?
            # need to convert month number - one less for regular years, after Adar
            if ((not isleap) and (month>6)):
                month = month-1;
            regular=0
            leap=0;

            for ii in range(yrs - 1): # for years _prior_ to this one
                if (ii in guachadazat):
                    leap = leap + 1
                else:
                    regular = regular + 1

            # okay, set various multiplies
            multipliers = [];
            multipliers.append(1);
            multipliers.append(cycles);
            multipliers.append(regular);
            multipliers.append(leap);
            multipliers.append(month-1); # for the beginning of the month, so Tishrei is 0, etc.
            return self.sumup(multipliers);

    def get_numeric_month_year(self, date, changeAdarOrder=True):
        j = hdate.converters.gdate_to_jdn(date);
        h = hdate.converters.jdn_to_hdate(j);

        # rearrange month number to put Adars back in middle
        m = hdate.htables.Months(h.month).value;
        if changeAdarOrder:
            if m == 13:
                m = 6
            elif m == 14:
                m = 7
            elif (m > 6):
                m = m + 1

        return {
            'year': h.year,
            'month': m,
        }

    def get_next_numeric_month_year(self, date, changeAdarOrder=True):
        d = self.get_numeric_month_year(date, changeAdarOrder);
        year = d['year'];
        month = d['month'];

        month = month + 1;

        if (month == 14):
            month = 1
            year = year + 1

        return {
            'year': year,
            'month': month
        }

    def get_day_of_week(self, numeric_date, day):    
        hebrew_date = hdate.HebrewDate(numeric_date['year'], numeric_date['month'], day)
        jdn_date = hdate.converters.hdate_to_jdn(hebrew_date);
        gdate = hdate.converters.jdn_to_gdate(jdn_date);
        weekday = gdate.strftime('%A');

        if weekday == 'Saturday':
            weekday = 'Shabbos';
        
        return weekday;

    def get_rosh_chodesh_days(self, date):
        this_month = self.get_numeric_month_year(date, False);
        next_month = self.get_next_numeric_month_year(date, False);

        next_month_name = hdate.htables.MONTHS[next_month['month'] - 1][False];

        # no Rosh Chodesh Tishrei
        if next_month['month'] == 1:
            return {
                'month': next_month_name,
                'text': '',
                'days': [],
            }
        
        first = self.get_day_of_week(this_month, 30);
        second = self.get_day_of_week(next_month, 1);

        if first == second:
            return {
                'month': next_month_name,
                'text': first,
                'days': [first],
            }
        else:
            return {
                'month': next_month_name,
                'text': first + " & " + second,
                'days': [first, second],
            }

    def is_shabbos_mevorchim(self, date) -> bool:
        loc = self.get_current_location();
        j = hdate.converters.gdate_to_jdn(date);
        h = hdate.converters.jdn_to_hdate(j);
        z = hdate.Zmanim(date=date, location=loc, hebrew=False)

        return self.is_actual_shabbat(z) and h.day >= 23 and h.month != hdate.htables.Months.Elul;

    def is_actual_shabbat(self, z) -> bool:
        today = hdate.HDate(gdate=z.date, diaspora=z.location.diaspora)
        tomorrow = hdate.HDate(gdate=z.date + datetime.timedelta(days=1), diaspora=z.location.diaspora)

        if (today.is_shabbat) and (z.time < z.havdalah):
            return True
        if (tomorrow.is_shabbat) and (z.time >= z.candle_lighting):
            return True

        return False

    def get_current_location(self) -> Location:
        return Location(
            latitude=self.get_plugin_config()['latitude'],
            longitude=self.get_plugin_config()['longitude'],
            timezone=self.get_plugin_config()['time_zone'],
            diaspora=True,
        )

    def refresh_molad_task(self, event):
        return self.refresh_molad()

    def refresh_molad(self):
        d = datetime.date.today()

        m = self.get_molad(d)
        rc = self.get_rosh_chodesh_days(d)
        sm = self.is_shabbos_mevorchim(d)

        self.set_state('sensor.molad', state=m['text'], attributes={
            'icon': 'mdi:moon-waxing-crescent',
            'friendly_name': 'Molad',
            'period': m['period'],
            'day': m['day'],
            'hours': m['hours'],
            'minutes': m['minutes'],
            'am/pm': m['am/pm'],
            'chalakim': m['chalakim'],
            'friendly': m['text'],
            'rosh_chodesh': rc['text'],
            'rosh_chodesh_days': rc['days'],
            'is_shabbos_mevorchim': sm,
            'month_name': rc['month'],
        }, replace=True)

        self.set_state('sensor.is_shabbos_mevorchim', state=sm);

        self.log('Molad Refreshed')
