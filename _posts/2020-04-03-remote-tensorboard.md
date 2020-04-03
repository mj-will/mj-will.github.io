---
title: "Using Tensorboard on a remote cluster"
tags:
  - python
  - tensorboard
  - ssh
  - bash
---

Tensorboard is an incredibly useful tool that allows you to monitor models deployed in Tensorflow or PyTorch as they train and provides are clear interface. If you're using it on a remote machine you'll need to setup port fowarding to your local machine. This is pretty easy to do using SSH tunneling. This can quickly become tedious if you have to regulalry connect and disconnect the tunnel.

In this post I'll explain how I streamlined the whole process with a simple bash script. I'll be assuming some familiarity with SSH and bash.

## The goal

The end goal is script that allows us to simply start, check the status of and close a tunnel a particular host. We want it to be simple to use so all we need to specify is the host and action, something like this:

```
$ tensorboard-remote <remote-host> <action>
```

## Tensorboard on the remote machine

For the purposes of this example we'll assume everything is setup for Tensorboard and it just needs to be started. The default port for Tensorboard is 6006, in general it's a good idea to change this to a different port to be slightly more secure, for this example we'll use 6008. Also note that if this port is already in use this will not work. We then start tensorboard like so:

```
$ tensorboard --logdir ./logdir --port 6008
```

## Managing ssh connections

Skip ahead to [this section](the-script) if you just want to see the final script.

### A simple approach

We need to open SSH tunnel the host in question and forward a particular port to our local machine, the simplest way to do this would be something like:

```
$ ssh -N -f -L localhost:6006:localhost:6008 remote_user@remote_host
```

This would foward port 6008 from the remote_host to port 6006 on your local machine. The `-L` option is the port fowarding configuration, `-N` indicates there will be no remote commands and `-f` sends the process to the background. This will work fine, but in order to end the process you'll need to kill it with its PID.

### More control with Multiplexing

[Multiplexing](https://en.wikibooks.org/wiki/OpenSSH/Cookbook/Multiplexing) allows for more control when it comes to managing SSH connections, I won't cover the details here but for those interested the previous link is worth a look. The aspect of multiplexing that interests us is the ability to manage SSH connections using a ControlMaster and ControlPath which determine how a control socket is used and where it will be located.

We can start an SSH connection with a ControlMaster using `-M` and specify a ControlPath with `-S`

```
$ ssh -M -S ~/.ssh/controlmasters/user@my.server.org:22 my.server.org
```

This will start a connection to `my.server.org` with a control socket saved to `~/.ssh/controlmasters/user@my.server.org:22`. We could check the status of the this connection using:

```
$ ssh -O check -S ~/.ssh/controlmasters/user@my.server.org:22 my.server.org
```

Finally we can exit using

```
$ ssh -O stop -S ~/.ssh/controlmasters/user@my.server.org:22 my.server.org
```

Note we could also use `%r@%h:%p` (remote user name)@(remote host):(remote host's port) to make things more general and cleaner.

### SSH config

The SSH configuration file, default location `~/.ssh/config` allows us to specify hosts that we can connect and makes the commands simpler. A typical host in the config file will look like this:

```
Host hostA
    HostName hostA.server.org
    User alice
    Port 22
```

You can the connect to `hostA`  using:

```
$ ssh hostA
```

We'll use this to simply the input to our final script.


## The script

Let's start writing out script. I'll call it `tensorboard-remote.sh` in this example and we'll have two command line arguments, the host and the task. The three tasks we want are: start, check and ecit. So let's layout the outline of the script with a set of if statements:

```bash
#!/usr/bin/env bash

port=6008
host=$1

if [ "$2" = "start" ]; then
    echo "Starting tunnel to $host for tensorboard"
elif [ "$2" = "check" ]; then
    echo "Checking tunnel to $host for tensorboard"
elif [ "$2" = "exit" ]; then
    echo "Exiting tunnel to $host for tensorboard"
else
    echo "Unknown task: $2"
fi
```

I've hard coded the port since I'll only be using this script for one machine with Tensorboard always running on the same port but this could easily be added as anther arugment. 

Now we just need to fill in each of the statements with ssh commands to start the tunnel, check it and exit it:

```bash
#!/usr/bin/env bash

port=6008
host=$1

if [ "$2" = "start" ]; then
    echo "Starting tunnel to $1 for tensorboard"
    ssh -M -S ~/.ssh/controlmasters/tb-%r@%h:%p -fNL 6006:localhost:$port $host
elif [ "$2" = "check" ]; then
    echo "Checking tunnel to $host for tensorboard"
    ssh -S ~/.ssh/controlmasters/tb-%r@%h:%p -O check $host
elif [ "$2" = "exit" ]; then
    echo "Exiting tunnel to $host for tensorboard"
    ssh -S ~/.ssh/controlmasters/tb-%r@%h:%p -O exit $host
else
    echo "Unknown task: $2"
fi

```
Here we've used portforwarding when start the ControlMaster to forward the port on the remote machine to port 6006 on our local machine. Notice we've also added `tb-` to the names of sockets, this differentiates them from any you may have for the same host that you don't want to be used to Tensorboard. This script would work as is, but you run this risk of starting multiple connections and then not being able to correctly exit the tunnels, so let's add a statement to check if there's
an existing connection already:

```bash
#!/usr/bin/env bash

port=6008
host=$1

if [ "$2" = "start" ]; then
    echo "Starting tunnel to $host for tensorboard"
    ssh -q -S ~/.ssh/controlmasters/tb-%r@%h:%p -O check $host
    if [ $? = 0 ]; then
        echo "Failed to start tunnel because control master already exists, either exist the process with tensorboard-remote $host exit or kill the process" 
    else
        ssh -M -S ~/.ssh/controlmasters/tb-%r@%h:%p -fNL 6006:localhost:$port $host
        echo "Tunnelling started"
    fi
elif [ "$2" = "check" ]; then
    echo "Checking tunnel to $host for tensorboard"
    ssh -S ~/.ssh/controlmasters/tb-%r@%h:%p -O check $host
elif [ "$2" = "exit" ]; then
    echo "Exiting tunnel to $host for tensorboard"
    ssh -S ~/.ssh/controlmasters/tb-%r@%h:%p -O exit $host
else
    echo "Unknown task: $2"
fi
```
And that's the finished product. We now just need to make the script executable with `chmod`:

```
$ chmod +x tensorboard-remote.sh
```

We can now start a tunnel from the local directory the script is in using:

```
$ ./tensorboard-remote hostA start
```

We can check on the status:

```
$ ./tensorboard-remote hostA check
```

And exit:

```
$ ./tensorboard-remote hostA exit
```

## Futher improvments

I would recommend moving this script to a directory which is in you `$PATH` or adding a directory to your `$PATH` (I normally use `~/.local/bin/`). This allows you to use the scirpt from any directory which is often handly. You could also easily add improvments like openning a tab in your browser that loads a connections to `http://localhost:6006/` or allowing the port to be an option.

## Conclusion

Tensorboard is a great tool for monitoring long jobs but setting up the port forwarding can be tedious. A script like the one shown here makes this simple and easy and removes the need to manually manage hosts, ports and open connections.
