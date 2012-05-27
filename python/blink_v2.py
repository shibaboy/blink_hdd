#!/usr/bin/python
# Aug 22 2011
# Made By shibaboy
# Ver 2.0


import sys, getopt, os, string, time
from subprocess import *

options, args = getopt.getopt(sys.argv[1:], 'o:f:w:')
for op, p in options:
	if op == '-o':
		print 'option LED ON', p
                disk = p
                todo = op
        elif op == '-f':
                print 'option LED OFF', p
                disk = p
                todo = op
        elif op == '-w':
                print 'option DISK WHERE', p
                disk = p
                todo = op
        else:
                print 'unknown option', op


def find_enclo():
	pipe = Popen('ls -al ../jbods/ | grep ses| awk {\'print $9\'}', shell=True, stdout=PIPE)
	enclo_no = pipe.stdout.read().strip().replace('\n',',')
	enclo_no = enclo_no.split(',')
	return enclo_no


def where(disk, enclo_no):
	enclo = ''
	sig = '0x500'
	diskcount = 0
	f = open('/root/blink_hdd/disks/%s' % disk)
	for line in f:
        	if sig in line:
                	#enclo = line[7:25]
                	diskcount += 1
                	if diskcount == 2:
                        	enclo = line [7:25]
                	else:
                        	pass
        	else:
                	pass
	f.close()


	#ses_count = enclo_no
	#for a in ses_count:
	ses_count = []
	ses_count = enclo_no
	for a in ses_count:
		f = open('/root/blink_hdd/jbods/%s' %a)
		for line in f:
			if enclo in line:
				enclosure = a
				pipe = Popen(['cat /root/blink_hdd/jbods/%s | egrep -B6 %s | egrep "bay number" | awk \'{print $11}\'' %(a, enclo)], shell=True, stdout = PIPE)
				bay = pipe.stdout.read().strip()
			else:
				pass
	
	print enclosure
	print bay
	
	return enclosure, bay

def pathadd():
	DISK_LIB_PATH = '/root/blink_hdd/lib/.libs'
	LD_LIBRARY_PATH = os.environ.get('LD_LIBRARY_PATH', '')

	if DISK_LIB_PATH not in LD_LIBRARY_PATH:
		os.environ['LD_LIBRARY_PATH'] = \
		os.pathsep.join([LD_LIBRARY_PATH, DISK_LIB_PATH]).lstrip(os.pathsep)
		os.execv(sys.executable, [sys.executable] + sys.argv)


def disk_on(enclosure, bay):
        pipe = Popen(['/root/blink_hdd/src/sg_ses -p 0x2 -f --raw /dev/es/%s > /root/blink_hdd/python/work/%s'%(enclosure, enclosure)], shell=True, stdout=PIPE)
        time.sleep(0.5)
	temp=''
        f=open('/root/blink_hdd/python/work/%s'%enclosure)
        for line in f:
                temp+=line[8:56]
                temp+='\n'
	print temp
	if bay == "0":
		temp = temp[:25] + '81 00 02 20' + temp[36:]
        elif bay == "1":
		temp = temp[:37] + '81 00 02 20' + temp[48:]
        elif bay == "2":
		temp = temp[:49] + '81 00 02 20' + temp[60:]
        elif bay == "3":
		temp = temp[:61] + '81 00 02 20' + temp[72:]
        elif bay == "4":
		temp = temp[:74] + '81 00 02 20' + temp[85:]
	elif bay == "5":
		temp = temp[:86] + '81 00 02 20' + temp[97:]
	elif bay == "6":
		temp = temp[:98] + '81 00 02 20' + temp[109:]
	elif bay == "7":
		temp = temp[:110] + '81 00 02 20' + temp[121:]
	elif bay == "8":
		temp = temp[:123] + '81 00 02 20' + temp[134:]
	elif bay == "9":
		temp = temp[:135] + '81 00 02 20' + temp[146:]
	elif bay == "10":
		temp = temp[:147] + '81 00 02 20' + temp[158:]
	elif bay == "11":
		temp = temp[:159] + '81 00 02 20' + temp[170:]
	else:
                print "not here.\n"
	f.close()
        print temp
        f=open('./work/on.txt','w')
	f.writelines(temp)
        f.close()
	pipe = Popen(['/root/blink_hdd/src/sg_ses --control -p 0x2 -d - /dev/es/%s < /root/blink_hdd/python/work/on.txt'%enclosure], shell=True, stdout=PIPE)
        print 'Enclosure : ',enclosure
	print 'Bay       : ',bay
        print 'It\'t on!!'


def disk_off(enclosure, bay):
	pipe = Popen(['/root/blink_hdd/src/sg_ses -p 0x2 -f --raw /dev/es/%s > /root/blink_hdd/python/work/%s'%(enclosure, enclosure)], shell=True, stdout=PIPE)
	time.sleep(0.5)
	temp=''
	f=open('/root/blink_hdd/python/work/%s'%enclosure)
	for line in f:
		temp+=line[8:56]
		temp+='\n'
	print temp
        if bay == "0":
		temp = temp[:25] + '80 00 00 00' + temp[36:]
        elif bay == "1":
		temp = temp[:37] + '80 00 00 00' + temp[48:]
	elif bay == "2":
		temp = temp[:49] + '80 00 00 00' + temp[60:]
	elif bay == "3":
		temp = temp[:61] + '80 00 00 00' + temp[72:]
	elif bay == "4":
		temp = temp[:74] + '80 00 00 00' + temp[85:]
	elif bay == "5":
		temp = temp[:86] + '80 00 00 00' + temp[97:]
	elif bay == "6":
		temp = temp[:98] + '80 00 00 00' + temp[109:]
	elif bay == "7":
		temp = temp[:110] + '80 00 00 00' + temp[121:]
        elif bay == "8":
		temp = temp[:123] + '80 00 00 00' + temp[134:]
	elif bay == "9":
		temp = temp[:135] + '80 00 00 00' + temp[146:]
	elif bay == "10":
		temp = temp[:147] + '80 00 00 00' + temp[158:]
	elif bay == "11":
		temp = temp[:159] + '80 00 00 00' + temp[170:]
	f.close()
        print temp
        f=open('./work/off.txt','w')
	f.writelines(temp)
        f.close()
	pipe = Popen(['/root/blink_hdd/src/sg_ses --control -p 0x2 -d - /dev/es/%s < /root/blink_hdd/python/work/off.txt'%enclosure], shell=True, stdout=PIPE)
        print 'Enclosure : ',enclosure
	print 'Bay       : ',bay
        print 'It\'s off!!'


if todo == '-w':
	c = find_enclo()
	where(disk, c)
elif todo == '-o':
	c = find_enclo()
	a, b = where(disk, c)
	pathadd()
	disk_on(a, b)
elif todo == '-f':
	c = find_enclo()
	a, b = where(disk, c)
	pathadd()
	disk_off(a, b)
else:
	sys.exit(1)
