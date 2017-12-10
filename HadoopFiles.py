import urllib2
import urllib
import os

files  = urllib2.urlopen('http://data.gdeltproject.org/gdeltv2/masterfilelist.txt')
web = files.read()

#Creating a file with the urls
myfile = open("myfiles.txt","w")
myfile.write(web)
myfile.close()

#Open the file in read mode
urls = open("myfiles.txt","r")
urlslist = urls.readlines()
urls.close()

#Open a file to save gkg urls
gkgurls = open("gkgfiles.txt","w")

for url in urlslist:
 url = url.split(" ")
 try:
  file = url[2]
  if "gkg" not in file:
   continue
  gkgurls.write(file)
 except:
  print("ERROR")

#Closing the file of gkg urls
gkgurls.close()

#Now we load the urls and download all the data
dataurls = open("gkgfiles.txt","r")
dataurls = dataurls.readlines()

#We can add a progressbar later

#Starting hadoop cluster
os.system("/usr/local/hadoop/sbin/start-dfs.sh")

for url in dataurls:
 names = url.split("/")
 filename = names[4]
 year = filename[0:4]
 month = filename[4:6]
 day = filename[6:8]
 #print(year,month,day)

 #print(filename)
 
 #Due to size limitations in Googles instances we will only use 2016 and 2017 data
 yearlist = ["2016"]
 if year not in yearlist:
  #print("Passing")
  continue  	
 
 monthlist = ["01"]
 if month not in monthlist:
  #print("Passing")
  continue

 daylist = ["01"]
 if day not in daylist:
  #print("Passing")
  continue

 try:
  os.system("rm -rf /usr/local/hadoop/tmp/Files")
 except:
  print("Directory doesn't exist")

 #Creating the file directories
 if not os.path.exists('/usr/local/hadoop/tmp/Files'):
  os.makedirs('/usr/local/hadoop/tmp/Files')

 if not os.path.exists('/usr/local/hadoop/tmp/Files/' + year):
  os.makedirs('/usr/local/hadoop/tmp/Files/' +  year)

 if not os.path.exists('/usr/local/hadoop/tmp/Files/'+year+"/"+month):
  os.makedirs("/usr/local/hadoop/tmp/Files/"+year+"/"+month)

 if not os.path.exists('/usr/local/hadoop/tmp/Files/'+year+"/"+month+"/"+day):
  os.makedirs("/usr/local/hadoop/tmp/Files/"+year+"/"+month+"/"+day)
 
 #Downloading file in the corresponding directory
 urllib.urlretrieve(url,"/usr/local/hadoop/tmp/Files/"+year+"/"+month+"/"+day+"/"+filename)

 #Unzipping the file
 os.system("unzip "+"'/usr/local/hadoop/tmp/Files/"+year+"/"+month+"/"+day+"/"+filename+"'"+" -d"+" /usr/local/hadoop/tmp/Files/"+year+"/"+month+"/"+day+"/")

 #Deleting the zip file
 os.system("rm "+"'/usr/local/hadoop/tmp/Files/"+year+"/"+month+"/"+day+"/"+filename+"'")

 #Before copying the files into hadoop file system we need to start the cluster
 #os.system("/usr/local/hadoop/sbin/start-dfs.sh")

 #Copying the file into hadoop file system
 #os.system("hdfs dfs -copyFromLocal"+" '/usr/local/hadoop/tmp/Files/"+year+"/"+month+"/"+day+"/"+filename+"'"+" '/user/hduser/Files/"+year+"/"+month+"/"+day+"/"+filename"'")
 
 #Creating the directory for our files in the hadoop file system
 os.system("hdfs dfs -mkdir -p /home/hduser/Files/"+year+"/"+month+"/"+day)

 os.system("hdfs dfs -copyFromLocal "+"/usr/local/hadoop/tmp/Files/"+year+"/"+month+"/"+day+"/"+filename+" /home/hduser/Files/"+year+"/"+month+"/"+day+"/"+filename)

#Closing the clsuter
os.system("/usr/local/hadoop/sbin/stop-dfs.sh")
