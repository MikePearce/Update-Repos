#! /usr/bin/python

#####
# This script will update all the repos on your dev container
#####



# Grab some functionality
import sys, os, glob

# Setup some stuff
args 		= sys.argv
# What is the root folder where your svn repos live
sites_dir 	= "/home/sites"
# Set a prepend if you only want to update certain repos
prepend 	= ""
#Do you want to create code coverage?
x = 1
os.system('clear')

# Check some stuff exists
try: args[1]
except IndexError:
	sys.stderr.write(" \t[[Either use 'up' to update or 'ci' to commit]]\n")
	sys.exit(1)
	svn_command = 'x'
else:
	svn_command = args[1]

if svn_command == 'ci':
	commit_message = raw_input("Please type a commit message:\n")


# Make results a list
results = {}

sys.stdout.write(" -- Welcome to the Mike Pearce python update/commit program -- \n");
print "Please wait, this may take a while..."

for infile in glob.glob(os.path.join(sites_dir, prepend +"*") ):
	if svn_command == "up":
		# Get the repo name
		file_array = infile.split("/")
                repo_name = file_array.pop()
		this_repo_results = {}
		this_repo_results['failmessage'] = {}

		## Run the svn update and print the result
		cmd = "cd "+ infile +";svn up;"
		fin, fout = os.popen4(cmd)
		result = fout.read()
		if result.find("At revision") != -1:
			this_repo_results['up'] = 'WINN'
		else:
			this_repo_results['up'] = 'FAIL'
			this_repo_results['failmessage'][len(this_repo_results['failmessage'])+1] = result

		# Find out if there is a unittests dir
		if os.path.exists(infile +"/unittests"):
			# Do the coverage
			cmd = "cd "+ infile +"; phpunit --coverage-html "+ sites_dir +"/codecoverage/"+ repo_name +"/ unittests/"
                	fin, fout = os.popen4(cmd)
	                result = fout.read()
			
			if result.find("failure:") != 1:
				this_repo_results['unit'] = 'PASS'
			else:
				this_repo_results['unit'] = 'FAIL'
				this_repo_results['failmessage'][len(this_repo_results['failmessage'])+1] = result

			this_repo_results['coverage'] = 'PASS'
		else:
			this_repo_results['coverage'] = 'NONE'
			this_repo_results['unit'] = 'NONE'
		# Now get the vhost
		if os.path.exists(infile +"/vhost.conf"):
			cmd = "cd "+ infile +"; cp vhost.conf /home/vhosts/"+ repo_name +".conf"
			fin, fout = os.popen4(cmd)
			this_repo_results['vhost'] = 'PASS'
		else:
			this_repo_results['vhost'] = 'NONE'

		results[repo_name] = this_repo_results


	elif svn_command == "ci":
		print "Committing: "+infile
                ## Run the svn update and print the result
                cmd = "cd "+ infile +";svn ci -m'" + commit_message + "'"
                fin, fout = os.popen4(cmd)
                result = fout.read()
		if result == '':
			print "Not committed, nothing changed"
		else:
	                print result

	if x == 1:
		if svn_command == 'up':

			print "               ,'``.._   ,'``."
			print "              :,--._:)\,:,._,.:       All Glory to"
			print "              :`--,''   :`...';\      the HYPNO TOAD!"
			print "               `,'       `---'  `.   "+ repo_name
			print "               /                 :"
			print "              /                   \\"
			print "            ,'                     :\.___,-."
			print "           `...,---'``````-..._    |:       \\"
			print "             (                 )   ;:    )   \  _,-."
			print "              `.              (   //          `'    \\"
			print "               :               `.//  )      )     , ;"
			print "             ,-|`.            _,'/       )    ) ,' ,'"
			print "            (  :`.`-..____..=:.-':     .     _,' ,'"
			print "             `,'\ ``--....-)='    `._,  \  ,') _ '``._"
			print "          _.-/ _ `.       (_)      /     )' ; / \ \`-.'"
			print "         `--(   `-:`.     `' ___..'  _,-'   |/   `.)"
			print "             `-. `.`.``-----``--,  .'"
			print "               |/`.\`'        ,','); "
			print "                   `         (/  (/"
			x = 2
	else:
		if svn_command == 'up':

			print "          |.--------_--_------------_--__--.| " + repo_name
			print "          ||    /\ |_)|_)|   /\ | |(_ |_   ||"
			print "          ;;`,_/``\|__|__|__/``\|_| _)|__ ,:|"
			print "         ((_(-,-----------.-.----------.-.)`)"
			print "          \__ )        ,'     `.        \ _/"
			print "          :  :        |_________|       :  :"
			print "          |-'|       ,'-.-.--.-.`.      |`-|"
			print "          |_.|      (( (*  )(*  )))     |._|"
			print "          |  |       `.-`-'--`-'.'      |  |"
			print "          |-'|        | ,-.-.-. |       |._|"
			print "          |  |        |(|-|-|-|)|       |  |"
			print "          :,':        |_`-'-'-'_|       ;`.;"
			print "           \  \     ,'           `.    /._/"
			print "            \/ `._ /_______________\_,'  /"
			print "             \  / :   ___________   : \,'"
			print "              `.| |  |           |  |,'"
			print "                `.|  |           |  |"
			print "                  |  |           |  |"
			x = 1

# Now we can create an index.php in the covereage folder
html = "<h1>Code coverage</h1>"
for infile in glob.glob(os.path.join("/home/sites/codecoverage", "*")):
	file_array = infile.split("/")
	dir = file_array.pop()
	if dir != 'index.html':
		html = html + "<a href='"+ dir +"'>"+ dir +"</a><br />"

# Got HTML? Good
filename = "index.html"
 
#print "Writing to file: %s" % filename
 
 
file = open("/home/sites/codecoverage/" +filename, 'w')
file.write(html)
file.close()

#get the hostname
fin, fout = os.popen4("hostname")
hostname = fout.read()

# Now lets see if there's a vhost
vhost_file = "/home/vhosts/coverage.conf"

vhost = '<VirtualHost *:80>\n'
vhost = vhost + 'DocumentRoot    /home/sites/codecoverage\n'
vhost = vhost + 'ServerName      coverage.'+ hostname +'\n'
vhost = vhost + '</VirtualHost>\n'

file = open(vhost_file, 'w')
file.write(vhost)
file.close()

# Restart apache
os.system('sudo /sbin/service httpd reload')

#print "Vhost installed and apache reloaded"

print "Coverage Written, please visit: http://coverage."+ hostname

print "+--------------------+------------+---------+------------------+--------------------+"
print "|        repo        |  updated?  |  Unit?  |  Code Coverage?  |  vhost installed?  |"
print "+--------------------+------------+---------+------------------+--------------------+"
fail_messages = []
for item in results.items():
	key, value = item
	print "| "+ key.ljust(19) +"|  "+ value['up'] +"      |   "+ value['unit'] +"  | "+ value['coverage'] +"             |  "+ value['vhost'] +"              |"
	for x in value['failmessage'].items():
		fail_messages.append(key +": "+ x[1])
print "+--------------------+------------+---------+------------------+--------------------+"
print "\n"
print "+------------------------------- ERROR MESSAGES ------------------------------------+"
for item in fail_messages:
	print item
	#print key +": "+ value
print "\n\n"