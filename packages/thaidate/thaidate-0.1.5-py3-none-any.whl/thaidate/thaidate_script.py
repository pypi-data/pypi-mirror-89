from datetime import date

class thaidate:
    
    def __init__(self, value:date = None, Buddhist:bool = False) -> None:
        self.value:date = value
        self.Buddhist:bool = Buddhist
        self.value_date:list = []
        self.check_value()
        self.check_value_date()
        
    def check_value(self) -> None:
        if self.value in (None, ''):
            self.value = date.today()
        
        if isinstance(self.value, date):
            self.value_date = self.value.strftime('%Y %m %d').split()
        else:
            self.check_str_date()
            
    def check_str_date(self) -> None:
        try:
            if ' ' in self.value:
                self.value_date = self.value.split()
            elif '/' in self.value:
                self.value_date = self.value.split('/')
            elif '-' in self.value:
                self.value_date = self.value.split('-')
            else:
                raise Exception('คุณต้องกำหนดข้อมูลให้อยู่รูปแบบ yyyy mm dd, yyyy-mm-dd, yyyy/mm/dd เท่านั้น')
                
        except Exception as error:
            print('Caught this error: ' + repr(error))
            
    def check_value_date(self) -> None:
        if int(self.value_date[2]) < int(self.value_date[0]):
            self.value_date.reverse()
        if self.Buddhist == False:
            self.value_date[2] = int(self.value_date[2])+543
    
    @property   
    def day(self) -> int:
        return self.value_date[0]
    
    @property   
    def full_month(self) -> str:
        full_thai_month:tuple = ('มกราคม', 'กุมภาพันธ์', 'มีนาคม', 'เมษายน', 'พฤษภาคม', 'มิถุนายน', 'กรกฎาคม', 'สิงหาคม', 'กันยายน', 'ตุลาคม', 'พฤศจิกายน', 'ธันวาคม')
        return full_thai_month[int(self.value_date[1])- 1]
    
    @property
    def short_month(self) -> str:
        short_thai_month:tuple = ('ม.ค.', 'ก.พ.', 'มี.ค', 'เม.ษ.', 'พ.ค.', 'มิ.ย.', 'ก.ค.', 'ส.ค.', 'ก.ย.', 'ต.ค.', 'พ.ย.', 'ธ.ค.')
        return short_thai_month[int(self.value_date[1])- 1]
    
    @property  
    def year(self) -> int:
        return self.value_date[2]
    
    @property  
    def weekday(self) -> str:
        weekDays:tuple = ("วันอาทิตย์", "วันจันทร์","วันอังคาร","วันพุธ","วันพฤหัสบดี","วันศุกร์","วันเสาร์")
        date_week_day:date = date(int(self.value_date[2]), int(self.value_date[1]), int(self.value_date[0]))
        return weekDays[date_week_day.weekday() - 1]
    
    @property
    def date(self) -> str:
        return f'{self.day} {self.full_month} {self.year}'
    
    @property
    def short_date(self) -> str:
        return f'{self.day} {self.short_month} {self.year}'
    
    @property
    def full_date(self) -> int:
        return f'วัน{self.weekday}ที่ {self.day} เดือน{self.full_month} ปีพุทธศักราช {self.year}'
    
    @property
    def rattanakosin_era(self) -> int:
        return self.year - 2324