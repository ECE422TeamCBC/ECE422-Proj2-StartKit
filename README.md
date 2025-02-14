ECE 422: Reliable and Secure Systems Design, Project 1 Part 2,
by Carl Fang, Calvin Choi, Brandon Hoynick
Modified Instructions for AutoScaling Docker system to support simpleweb app:
(The original starter kit instructions are at the bottom of this readme).
=============
Deployment Instructions (and any user guides)
Note: You may require prefixing most commands with “sudo” depending on if the admin user is logged in.
1. Assure that the auto-scaler image is up to date. The image can be built and pushed by running the build.sh file in the auto-scaler directory.
1a. On the Server VM, in the auto-scaler directory, Run 
    ```bash
        ./build.sh 
    ```
    to build and push the updated image for the auto scaler.
2. Assure the web-app image is up to date. The image can be built and pushed by running the build.sh file in the web-app directory.
2a. On the Server VM, in the web-app directory,
    ```bash
        ./build.sh 
    ```
    to build and push the updated image for the web-app.
3. In order to deploy all the various microservices, run on Server VM the following:
    ```bash
        docker stack deploy --compose-file docker-compose.yml app_name
    ```
4. Initialize any number of client connections to the running server application, and explore all the various microservices. This can run on the Client VM with the original http_client.py:
    ```bash
        python3 http_client.py <swarm_manager_ip> <no users> <wait time>
    ```
    4a. Or with Locust:
    ```bash
        locust -f locustfile.py
    ```

(locust prompts to open http://localhost:8089 to see the Locust dashboard, where you can start the swarm and view the “Total Request per second”, the “Response Times (ms)”, and “Number of Users” ).

5. View on various monitoring systems the different available charts (Locust, Grafana on localhost:3000 for retrieving Redis database data, and Prometheus web scraper).

6. You should observe the autoscaler receive web statistical data which will check if response times are too high and tell Docker to scale up the amount of apps, or that response times are dropping to normal rates, so after a period tell Docker to scale down the amount of web apps.

----------------------------------------------------------------------------------------------------------------------------------------------
Our server side elements are located within the ‘Project1’ folder (which contains all microservice help apps for the web app serving system).

The ‘original-kit’ folder contains items from the starter kit (not used, just kept for the original reference).

The ‘ClientVM’ folder contains client simulator elements used in our project.

The Design folder contains: 
- A high-level architectural view of application auto-scalability features.
- A state diagram that shows the state, events, and actions in the auto-scaler.
- The pseudocode of the auto-scaling algorithm along with reasons behind the parameter settings in the algorithm.

=============
Original Starter Kit Instructions by  Zhijie Wang
=============
This repository provides the starter kit for the Reliability project. The `docker-images` folder
contains the Dockerfile, a simple application in `Python` and a requirement file including dependencies for
the application. This directory is for your information and reference as the image (simpleweb) has already been built and pushed to [Docker Hub](https://hub.docker.com/r/zhijiewang22/simpleweb) repository.

The following steps show how you can prepare the deployment environment on Cybera Cloud; briefly, you need to a) provision 
Virtual Machines (VMs) on Cybera b) install Docker on VMs c) create a Swarm cluster of at least two of 
VMs and d) deploy a web application on the Swarm cluster as microservices.

Also, this repository contains a base implementation of an HTTP client program that may be customized or extended 
according to your needs. 

Initial steps for accomplishing your project:   

1. Create 3 VMs on Cybera cloud with the following specifications:

    1. Use `Ubuntu 18.04` or `Ubuntu 20.04` as the image for all VMs.

    2. You need one of these VMs to run the client program for which you may use `m1.small` flavor. Let's call this VM as
the `Client_VM`.

    3. For the other two VMs, please still consider `m1.small` flavor. These two VMs will construct your Swarm cluster.

    4. You need to open the following TCP ports in the `default security group` in Cybera:
        - 22 (ssh), 2376 and 2377 (Swarm), 5000 (Visualization), 8000 (webapp), 6379 (Redis)
        - You can do this on Cybera by going to `Network` menu and `Security Groups`. ([See Here](./figures/sg.png))

2. On the `Client_VM` run
    ```bash
    $ sudo apt -y install python-pip
    $ pip install requests
    ```

3. Then, you need to install *Docker* on VMs that constitute your Swarm Cluster. Run the following on each node.
    ```bash
    $ sudo apt update
    $ sudo apt -y install docker.io
    ```
    
4. Now that Docker is installed on the two VMs, you will create the Swarm cluster.
    1. For the VM that you want to be your Swarm Manger run:
    ```bash
    $ sudo docker swarm init
    ```

    2. The above `init` command will produce something like the bellow command that you need to run on all worker nodes.
    ```bash
    $ docker swarm join \
        --token xxxxxxxxxxxxxxxxxx \
        swarm_manager_ip:2377
    ```
    3. Above command attaches your worker to the Swarm cluster.
5. On your Swarm manager, download the docker-compose.yml file:
    ```bash
    $ wget https://raw.githubusercontent.com/zhijiewang22/ECE422-Proj2-StartKit/master/docker-compose.yml
    ```
6. Run the following to deploy your application:
    ```bash
    $ sudo docker stack deploy --compose-file docker-compose.yml app_name
    ```
7. Your deployed application should include three microservices:
    1. A visualization microservice that is used to visualize the Swarm cluster nodes and the running microservices. 
        - Open `http://swarm_manager_ip:5000` in your browser. Note that you should have the Cybera VPN client 
    running in order to see the page. ([Sample](./figures/vis.png))
    2. A web application that is linked to a Redis datastore. This simple application shows the number that it has 
    been visited and the period that took it to solve a hard problem. 
        - Open `http://swarm_manager_ip:8000` to see the web application. Try to refresh the page. You should see the hitting number increase one by one and also the computation time change each time. ([Sample](./figures/app.png))
    3. A Redis microservice which in fact doesn't do anything fancy but return the number of hitting.

8. Now, login into your `Client_VM` and download the http client program:
    ```bash
    $ wget https://raw.githubusercontent.com/zhijiewang22/ECE422-Proj2-StartKit/master/http_client.py
    ```
9. Then run the `http_client.py` program with one user who sends a request, waits for response, when received the 
    response would think for one second, and then send another request. This cycle goes on as long as the client 
    program is running.
    ```bash
    $ python3.5 http_client.py swarm_manager_ip 1 1
    ```
    1. The program should print the response time for each request.
    2. Generally, this client program creates a number of users that send requests to the server and after receiving 
    the response thinks for the amount of `think_time` and then sends a new request.
    3. If you increase the number of users or decrease the think time, ie increasing the workload, the response 
    time should increase.
    4. **Important Note**: for development and testing purposes you may run the client program on your laptop 
    which is a reasonable strategy. However, running the client program for a long time on your laptop might appear as 
    a DoS attack to Cybera firewall which may result in unexpected outcomes for your VMs. Therefore, try to run the 
    http client program on the `Client_VM`.
    
    
 Good Luck!
