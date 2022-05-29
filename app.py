#import necessary packages
from flask import Flask,render_template, url_for
import csv
import matplotlib
import matplotlib.pyplot as plt
import os

# the computation to be done in case of features that have numerical values
def numerical(no): #it takes the column index as an argument
      with open('cars_engage_2022.csv', 'r') as datafile: #csv package to open csv file
            reader= csv.reader(datafile)
            row=[]
            temp=[]
            for i in reader:
                  row.append(i) #append all the rows to a last for future access
                  if i[1]!="Make": #append all values in the particular column expect the header row to a list
                        temp.append(i[no])
                        temp=list(set(temp))
             #remove null values
                  if '' in temp:
                        temp.remove('')
            # the data values are in string form which include units(eg.Rs etc) that need to be removed 
            for x in range(0,len(temp)):
                  temp[x]=str(temp[x]).replace("Rs. ",'')
                  temp[x]=str(temp[x]).replace(',','')
                  temp[x]=str(temp[x]).replace(" cc",'')
                  temp[x]=str(temp[x]).replace(" mm",'')
                  temp[x]=str(temp[x]).replace(" litres",'')
                  temp[x]=str(temp[x]).replace(" km/litre",'')
                  temp[x]=str(temp[x]).replace(" kg",'')
                  temp[x]=str(temp[x]).replace("kg",'')
                  temp[x]=str(temp[x]).replace("NA",'0')
                  temp[x]=str(temp[x]).replace('?','')
                  if no==20 or no==21 or no==22:
                        temp[x]=str(temp[x][:2]) #columns 20-22 contain ranges and hence only the minimum in considered
                  temp[x]=float(temp[x]) #convert to float so that computation can be done
            f=open('static/output.txt','w')
            #code to compute mean
            mean = sum(temp) / len(temp)
            #code to compute variance
            var = sum([((x - mean) ** 2) for x in temp]) / len(temp)
            #standard deviation 
            res = var ** 0.5
            f.write("The mean of the data is ")
            f.write(str(mean))
            f.write('\n'+"The standard deviation for the data is ")
            f.write(str(res))
            f.write('\n'+"The min value for the data is ")
            f.write(str(min(temp)))
            f.write('\n'+"The max value for the data is ")
            f.write(str(max(temp)))
            # to write web.html depending on the feature to be analysed
            webpg=open("templates/web.html",'w')
            wr1=open("templates/dupl.html",'r')
            webpg.write(wr1.read())
            webpg.write(row[0][no])
            wr2=open("templates/dupl1.html",'r')
            webpg.write(wr2.read()) 
            #web.html is written using 2 segments present in dupl.html and dupl1.html 

# the computation to be done in case of features that have numerical values
def unique(no):
      with open('cars_engage_2022.csv', 'r') as datafile: #csv package to open csv file
            reader= csv.reader(datafile)
            temp=[]
            row=[]
            for i in reader:
                  row.append(i) #append all the rows to a last for future access
                  if i[1]!="Make":
                        temp.append(i[no])
                        temp=list(set(temp)) #append all values in the particular column expect the header row to a list
            #remove null values
            if '' in temp:
                  temp.remove('') 
            #write the unique values to an output file which will later be embedded in the html page
            file=open('static/output.txt','w')
            file.write("There are ")
            file.write(str(len(temp))) 
            file.write(" different "+row[0][no]+'\n')
            file.write("They are "+'\n')
            file.write(str(temp))
            n=len(temp)
            num=[0]*n
            #find the number of instances of each element present in the dataset
            for i in row:
                  for k in range(0,len(temp)):
                        if i[no]==temp[k]:
                              num[k]+=1
            x,y=[],[]
            file.write('\n'+"number of cars of each "+row[0][no]+":"+'\n')
            for j in range(0,len(temp)):
                  file.write(temp[j]+":")
                  file.write(str(num[j])+'\n')
                  if num[j]>5: #only significant ones are plotted, if number  of instances is more than 5
                        x.append(temp[j])
                        y.append(num[j])
            #plot the graph of unique elements versus the number of instances of each elemnt
            plot1=plt.figure(1)
            plt.bar(x, y, color='g', label = "no of each")
            plt.xlabel(row[0][no])
            plt.ylabel('Number of instances')
            plt.xticks(rotation='vertical', fontsize=4)
            plt.title('number of each diff '+row[0][no]+'(more than 5 entries)')
            os.remove('static/plot.jpg') #remove the previous plot
            plot1.savefig('static/plot.jpg') #save the new plot
            #write the html page to be rendered using dupl.html and dupl2.html which embeds the output file and the graph
            webpg=open("templates/web.html",'w')
            wr1=open("templates/dupl.html",'r')
            webpg.write(wr1.read())
            webpg.write(row[0][no])
            wr2=open("templates/dupl2.html",'r')
            webpg.write(wr2.read())     
#flask app
app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/summary")
def summary():
      #csv package to get the summary of the dataset given
      with open('cars_engage_2022.csv', 'r') as datafile:
            reader= csv.reader(datafile)    
            colu=len(next(reader))
            datafile.seek(0)
            rows=len(datafile.readlines()) 
            f=open('static/summary.txt','w')
            f.write("There are "+str(rows)+ " rows in the datafile"+'\n')
            f.write("There are "+str(colu)+ " features in the datafile"+'\n')
            f.write("To analyse by feature, go to Analysis")
      return render_template("summary.html")

#routing to different webpages and rendering web.html according to the feature to be analysed
@app.route("/analysis")
def analysis():
      return render_template("analysis.html")
    
@app.route("/analysis/make")
def make():
      unique(1)
      return render_template('web.html') 

@app.route("/analysis/model")
def model():
      unique(2)
      return render_template('web.html')

@app.route("/analysis/variant")
def var():
      unique(3)
      return render_template('web.html')

@app.route("/analysis/price")
def price():
      numerical(4)
      return render_template('web.html')

@app.route("/analysis/displ")
def displ():
      numerical(5)
      return render_template('web.html')

@app.route("/analysis/cylinder")
def cylinder():
      numerical(6)
      return render_template('web.html')

@app.route("/analysis/valves")
def valves():
      numerical(7)
      return render_template('web.html')

@app.route("/analysis/drivetrain")
def drivetrain():
      unique(8)
      return render_template('web.html')

@app.route("/analysis/cyl_conf")
def cyl_conf():
      unique(9)
      return render_template('web.html')

@app.route("/analysis/emmisson")
def emission():
      unique(10)
      return render_template('web.html')

@app.route("/analysis/eng_loc")
def eng_loc():
      unique(11)
      return render_template('web.html')

@app.route("/analysis/fuel_sys")
def fuel_sys():
      unique(12)
      return render_template('web.html')

@app.route("/analysis/tank_capacity")
def tank():
      numerical(13)
      return render_template('web.html')

@app.route("/analysis/fuel_type")
def feul_type():
      unique(14)
      return render_template('web.html')

@app.route("/analysis/ht")
def ht():
      numerical(15)
      return render_template('web.html')

@app.route("/analysis/leng")
def leng():
      numerical(16)
      return render_template('web.html')

@app.route("/analysis/wdt")
def wdt():
      numerical(17)
      return render_template('web.html')

@app.route("/analysis/body_type")
def bod_type():
      unique(18)
      return render_template('web.html')

@app.route("/analysis/doors")
def doors():
      numerical(19)
      return render_template('web.html')

@app.route("/analysis/city_mil")
def city_mil():
      numerical(20)
      return render_template('web.html')

@app.route("/analysis/high_mil")
def high_mil():
      numerical(21)
      return render_template('web.html')

@app.route("/analysis/arai")
def arai():
      numerical(22)
      return render_template('web.html')

@app.route("/analysis/gears")
def gears():
      unique(25)
      return render_template('web.html')

@app.route("/analysis/gnd_clr")
def gnd_clr():
      numerical(26)
      return render_template('web.html')

@app.route("/analysis/fbrakes")
def fbrakes():
      unique(27)
      return render_template('web.html')

@app.route("/analysis/bbrakes")
def bbrakes():
      unique(28)
      return render_template('web.html')

@app.route("/analysis/fnt_susp")
def f_susp():
      unique(29)
      return render_template('web.html')

@app.route("/analysis/bk_susp")
def bk_susp():
      unique(30)
      return render_template('web.html')

@app.route("/analysis/f_track")
def ftrack():
      numerical(31)
      return render_template('web.html')

@app.route("/analysis/b_track")
def btarck():
      numerical(32)
      return render_template('web.html')

@app.route("/analysis/steer")
def steer():
      unique(35)
      return render_template('web.html')

@app.route("/analysis/pow_win")
def pow_win():
      unique(36)
      return render_template('web.html')

@app.route("/analysis/pow_seats")
def pow_seats():
      unique(37)
      return render_template('web.html')

@app.route("/analysis/keyless")
def keyless():
      unique(38)
      return render_template('web.html')

@app.route("/analysis/odometer")
def odometer():
      unique(41)
      return render_template('web.html')

@app.route("/analysis/speedometer")
def speedometer():
      unique(42)
      return render_template('web.html')

@app.route("/analysis/tachometer")
def tachometer():
      unique(43)
      return render_template('web.html')

@app.route("/analysis/tripmeter")
def tripmeter():
      unique(44)
      return render_template('web.html')

@app.route("/analysis/seat_capacity")
def seatcap():
      numerical(45)
      return render_template('web.html')

@app.route("/analysis/seat_material")
def seat_material():
      unique(46)
      return render_template('web.html')

@app.route("/analysis/type")
def type():
      unique(47)
      return render_template('web.html')

@app.route("/analysis/wheelbase")
def wheelbase():
      numerical(48)
      return render_template('web.html')

@app.route("/analysis/start_button")
def str_button():
      unique(50)
      return render_template('web.html')

@app.route("/analysis/pow_outlet")
def pow_out():
      unique(51)
      return render_template('web.html')

@app.route("/analysis/audiosys")
def audio():
      unique(52)
      return render_template('web.html')

@app.route("/analysis/aux_in")
def aux_in():
      unique(53)
      return render_template('web.html')

@app.route("/analysis/fuel_cons")
def fuel_cons():
      unique(54)
      return render_template('web.html')

@app.route("/analysis/warranty")
def warranty():
      unique(55)
      return render_template('web.html')

@app.route("/analysis/bluetooth")
def bluetooth():
      unique(56)
      return render_template('web.html')

@app.route("/analysis/bootlid_opener")
def bootlid():
      unique(57)
      return render_template('web.html')

@app.route("/analysis/bootspace")
def bootspace():
      unique(58)
      return render_template('web.html')

@app.route("/analysis/cd")
def cd():
      unique(59)
      return render_template('web.html')

@app.route("/analysis/central_lock")
def central_lock():
      unique(60)
      return render_template('web.html')

@app.route("/analysis/child_lock")
def child_lock():
      unique(61)
      return render_template('web.html')

@app.route("/analysis/clock")
def clock():
      unique(62)
      return render_template('web.html')

@app.route("/analysis/cup_holders")
def cup():
      unique(63)
      return render_template('web.html')

@app.route("/analysis/dist_empty")
def dist_empty():
      unique(64)
      return render_template('web.html')

@app.route("/analysis/door_pockets")
def door_pockets():
      unique(65)
      return render_template('web.html')

@app.route("/analysis/eng_light")
def eng_light():
      unique(66)
      return render_template('web.html')

@app.route("/analysis/ext_warranty")
def ext_warranty():
      unique(67)
      return render_template('web.html')

@app.route("/analysis/fm")
def fm():
      unique(68)
      return render_template('web.html')

@app.route("/analysis/fuellid_opener")
def feullid():
      unique(69)
      return render_template('web.html')

@app.route("/analysis/fuel_gauge")
def fuel_gauge():
      unique(70)
      return render_template('web.html')

@app.route("/analysis/handbrake")
def handbrake():
      unique(71)
      return render_template('web.html')

@app.route("/analysis/instr_cons")
def instr():
      unique(72)
      return render_template('web.html')

@app.route("/analysis/low_fuel_warn")
def lowfuel():
      unique(73)
      return render_template('web.html')

@app.route("/analysis/mult_displ")
def mult_displ():
      unique(75)
      return render_template('web.html')

@app.route("/analysis/sun_visor")
def sun_visor():
      unique(76)
      return render_template('web.html')

@app.route("/analysis/third_ac")
def thirdac():
      unique(77)
      return render_template('web.html')

@app.route("/analysis/vent_sys")
def vent_sys():
      unique(78)
      return render_template('web.html')

@app.route("/analysis/dim_rear")
def dim_rear():
      unique(79)
      return render_template('web.html')

@app.route("/analysis/hill_assist")
def hill_assist():
      unique(80)
      return render_template('web.html')

@app.route("/analysis/gear_indi")
def gear_indi():
      unique(81)
      return render_template('web.html')

@app.route("/analysis/immobiliser")
def immobiliser():
      unique(86)
      return render_template('web.html')

@app.route("/analysis/back_pockets")
def backpockets():
      unique(90)
      return render_template('web.html')

@app.route("/analysis/abs")
def abs():
      unique(93)
      return render_template('web.html')

@app.route("/analysis/headlight")
def headlight():
      unique(94)
      return render_template('web.html')

@app.route("/analysis/headrests")
def headrest():
      unique(95)
      return render_template('web.html')

@app.route("/analysis/gross_wt")
def gross_wt():
      numerical(96)
      return render_template('web.html')

@app.route("/analysis/airbag")
def airbag():
      unique(97)
      return render_template('web.html')

@app.route("/analysis/door_ajar")
def door_ajar():
      unique(98)
      return render_template('web.html')

@app.route("/analysis/ebd")
def ebd():
      unique(99)
      return render_template('web.html')

@app.route("/analysis/seat_belt")
def seat_belt():
      unique(100)
      return render_template('web.html')

@app.route("/analysis/gear_shift")
def gear_shift():
      unique(101)
      return render_template('web.html')

@app.route("/analysis/airbag_no")
def airbag_no():
      unique(102)
      return render_template('web.html')


@app.route("/analysis/adj_steer")
def ajd_steer():
      unique(104)
      return render_template('web.html')

@app.route("/analysis/park_assist")
def park_assist():
      unique(107)
      return render_template('web.html')

@app.route("/analysis/key_off")
def key_off():
      unique(108)
      return render_template('web.html')

@app.route("/analysis/usb")
def usb():
      unique(109)
      return render_template('web.html')

@app.route("/analysis/cigarette")
def cigarette():
      unique(112)
      return render_template('web.html')

@app.route("/analysis/infotainment")
def infotainment():
      unique(113)
      return render_template('web.html')

@app.route("/analysis/multifn_steer")
def multisteer():
      unique(114)
      return render_template('web.html')

@app.route("/analysis/avg_speed")
def avg_speed():
      unique(115)
      return render_template('web.html')

@app.route("/analysis/eba")
def eba():
      unique(116)
      return render_template('web.html')

@app.route("/analysis/seat_height")
def seat_height():
      unique(117)
      return render_template('web.html')

@app.route("/analysis/nav_system")
def nav_sys():
      unique(118)
      return render_template('web.html')

@app.route("/analysis/second_ac")
def sec_ac():
      unique(119)
      return render_template('web.html')

@app.route("/analysis/armrest")
def armrest():
      unique(121)
      return render_template('web.html')

@app.route("/analysis/ipod")
def ipod():
      unique(122)
      return render_template('web.html')

@app.route("/analysis/esp")
def esp():
      unique(123)
      return render_template('web.html')

@app.route("/analysis/glove_box")
def glove_box():
      unique(124)
      return render_template('web.html')

@app.route("/analysis/turbo")
def turbo():
      unique(127)
      return render_template('web.html')

@app.route("/analysis/isofix")
def isofix():
      unique(128)
      return render_template('web.html')

@app.route("/analysis/wiper")
def wiper():
      unique(129)
      return render_template('web.html')

@app.route("/analysis/leather_steer")
def leather_steer():
      unique(131)
      return render_template('web.html')

@app.route("/analysis/auto_headlamp")
def auto_headlamp():
      unique(132)
      return render_template('web.html')

@app.route("/analysis/asr")
def asr():
      unique(134)
      return render_template('web.html')

@app.route("/analysis/cruise")
def cruise():
      unique(135)
      return render_template('web.html')

#run the app on localhost, port 8080
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)
