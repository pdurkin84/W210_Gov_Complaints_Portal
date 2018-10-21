# Setting up and using a server with GPU for training

1. Login to the gateway server over ssh (key based logins only): 169.62.224.78
2. Set up the base install of the server.  Run:

        createtfsrv

    There are several levels of completion before the next stage can begin.  The steps occurring here are
	1. Server with GPU created, it's name will have each of our names first, then a random string
	2. Installation of various software packages and python packages is completing.  These include, git, tensorflow, finetune
	3. Download of this git repository into /W210_Gov_Complaints_Portal on the server

    When it completes a message with the hostname and "ready" will be printed on the terminal.  This means that you can login to the server, but the package installation is still ongoing.

3. Login to the server.  You will need to determine the IP address.  To do this (remember the hostname that was printed), do:

        slcli vs list

	This prints out all the servers along with their public and private IP addresses.  Recorder the public address as you will need this to connect directly from home, however from the gateway you can simply ssh (passwordlessly) to the private address to continue the setup. 
4. Check the progress of the installation.  Run the following, when this returns something the background installation of packages is complete.

        grep "W210: Completed stage 1 of installation" /var/log/syslog

    Note: It can take another 10-20 minutes to complete

5. Run two more scripts to set up CUDA drivers and protect the server with a firewall

        */W210_Gov_Complaints_Portal/Code/Softlayer/install_cuda.sh*
        */W210_Gov_Complaints_Portal/Code/Softlayer/install_iptables.sh*
	
	These run on the command line so once they have completed control will be returned to the terminal.  These take a while, probably 20 minutes, however once it is done the software is all installed.  Go to the next section on using the server for details on how to get in and get started.

6. Due to the costs and the fact that SoftLayer continue to charge even when the server is powered off, if the server is going to be down for a while we should delete it (section below).

## Logging in and using for coding

1.  All keys should be available on each server so if you can get in to the gateway you should be able to get into the new server.  You will need the *public ip address* to connect and create an ssh tunnel so that the ports for Jupyter Labs will be available on your local host.  To do this do:

        ssh -L 8888:127.0.0.1:8888 root@*IPAddressOfServer*

2.  Once you have logged in start Jupyter Labs in the project folder:

        cd /W210_Gov_Complaints_Portal
        jupyter lab --allow-root &

3.  Collect the URL that is output from the command, you can use this on the local browser of your laptop to connect.


## Deleting a server (with care, make sure it is the correct one)

1. Make sure any code is checked in:)
2. Get the id of the server with slcli:

        slcli vs list

3. Make sure you have the correct id and then type:

        slcli vs cancel ID

	This will prompt you to reenter the ID, do this and it will delete the server.


