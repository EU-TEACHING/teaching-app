<img src="https://teaching-h2020.eu/sites/default/files/teaching55.png" height="80">

## :warning: Work in progress :warning:


# :car: Teaching Platform :airplane:

A computing Toolkit for building Efficient Autonomous appliCations leveraging Humanistic INtelliGence is an EU-funded project that designs a computing platform and the associated software toolkit supporting the development and deployment of autonomous, adaptive and dependable CPSoS applications, allowing them to exploit a sustainable human feedback to drive, optimize and personalize the provisioning of their services.


## Modules
* Video feed module: 
  - Capture frames from video file or camera source and creates rtmp stream

* File sensor:
  - Reads a csv file and automatically sends the readings to the system in user defined intervals

* InfluxDB module:
  - Can subscribe to multiple topics and stores the measurements to a InfluxDB database

* Process module:
  - Is a wrapper that can be used execute user code in the system. For example can be used with a Machine Learning service to perform inference or training. That module have embedded the aggregation service.
* Shimmer module:
  - Raw data readings from shimmer devices (HR, EDA).

## Supported Platforms
Any Docker supported system.
* Linux :white_check_mark:
* Windows 10,11 under WSL2 :white_check_mark:
* IMX8 :warning:
* Other ARM64 boards :warning: 

:white_check_mark: **Working**
:warning:  **In progress**

## IMX8 Instructions :vertical_traffic_light:
For deployment on the IMX8 
Moving the docker directory to the external storage
```bash
 systemctl docker stop
 fdisk /dev/mmcblk1
 resize2fs /dev/mmcblk1p2
 cp -r /var/lib/docker /run/media/mmcblk1p2/var/lib/docker/
 rm -rf /var/lib/docker/
 ln -s /run/media/mmcblk1p2/var/lib/docker/ /var/lib/docker
 systemctl docker start
```
Install pip and update the docker-compose 

```bash
 python3 -m ensurepip
 python3 -m pip install --upgrade pip
 python3 -m pip uninstall docker-compose
 rm /usr/bin/docker-compose
 python3 -m pip install docker-compose
```

## Deployment
#### 1. Copy the repository to your system.
  ```bash
  git clone https://github.com/EU-TEACHING/TEACHING_Platform.git
  ```
#### 2. Based on platform you should build two images.
#### For ARM run the:
  ```bash
  basic_images/./create_ARM_images.sh
  ```
#### For x86/x64 run the:
  ```bash
  basic_images/./create_ARM_images.sh
  ```
## Usage

#### 1. Create a docker-compose file with your pipeline.
Take a look at the docker-compose examples, scenario_xx.yaml
#### 2. Start your expirement.
  ```bash
  docker-compose -f scenario_xx.yaml -up
  ```

## Custom module

#### 1. Code refactoring.
* Create a folder with your code and a main.py with the code below.
* Encapsulate your code inside the eval function.

```python
class Service_Model():

    def __init__(self,arg1,arg2.....):
      pass

    def eval(self,batch):
        '''
        Process the Batch data
        '''
        return [output]
```
The eval function has as input a batch of data. That batch is auto genarated from the aggregator service.  The batch size can be configured from the env variable of the Procces Module.
```python
#example of batch 1
[[np.array(),int,float,float,...]]

#example of batch n
[[np.array(),int,float,float,...],
[np.array(),int,float,float,...],
[np.array(),int,float,float,...],
.......]
```

The output of the eval can be anything. The format of the output is a list.
```python
[pred1,pred2,'hello']
```
It's important the number of the ouputs to be aligned with the number of topics on the output topic env variable.
Examples of custom modules can be found on modules/ai_modules/RL_predictor and modules/custom_modules/frame_metrics

#### 2. Create your Dockerfile.
  Create a Dckerfile with the name Dockerfile.your_module
  Based on your application you can use the teaching_image or teaching_image_Tensoflow.
  Examples of custom Dockerfiles are the Dockerfile.rl_predictor and Dockerfile.frame_metrics
#### 3. Create your pipeline.
  Create a docker-compose file with the name your_exp_name.yaml.
  Select our modules and using as template the scenario_2.yaml or scenario_3.yaml add your custom module to the file.

## Progress  

|Scenario|Description|x86/x64|IMX8|Other ARM|
|-|-|-|-|-|
|Scenario 1|Record measurements of a vehicle in a route.|:white_check_mark:|:white_check_mark:|:warning:|
|Scenario 2|Personalization of driving experience using a RL model.|:white_check_mark:|:warning:|:warning:|
|Scenario 3|Process real time video stream and draw the measurements on the image.|:white_check_mark:|:warning:|:warning:|
|Scenario 4|Record measurements of a driver usnig shimmer device.|:warning:|:warning:|:warning:|

:white_check_mark: **Tested**
:warning:  **Untested**

## Contributors   
<table border=0 >
  <tr >
    <td> Konstantinos Tserpes</br>
          Assistant Professor</br>
          Harokopio University</br>
          Informatics and Telematics</br> 
          <a>https://github.com/tserpes</a></br>
          <a> tserpes@hua.gr</a></br>
          </td>   
    <td>Christos Chronis</br>
        Phd Candidate </br>
        Harokopio University</br>
        Informatics and Telematics</br>
        <a>https://github.com/chronis10</a></br>
        <a>chronis@hua.gr</a></br>
        </td>
  </tr>
</table>

## Partners
<table border=0 >
  <tr >
    <td> <img src="https://teaching-h2020.eu/sites/default/files/styles/mt_brands/public/2020-02/University-of-Pisa.png"  height="100"></td>   
    <td><img src="https://lowinfood.eu/wp-content/uploads/2021/01/HUA-Logo-Blue-RGB-1-1024x427.jpg"  height="130"></td>
    <td><img src="https://teaching-h2020.eu/sites/default/files/styles/mt_brands/public/2020-02/CNR.png" height="80"></td>
  </tr>
  <tr >
  <td><img src="https://teaching-h2020.eu/sites/default/files/styles/mt_brands/public/2020-02/I%26M.png" height="80"> </td>
  <td><img src="https://teaching-h2020.eu/sites/default/files/styles/mt_brands/public/2020-02/TUG.png" height="80"></td>
  <td><img src="https://teaching-h2020.eu/sites/default/files/styles/mt_brands/public/2020-02/AVL-Logo.jpg" height="80"></td>

  </tr>
  <tr >
  <td><img src="https://teaching-h2020.eu/sites/default/files/styles/mt_brands/public/2021-04/marelli-logo-history.png" height="80"></td>
  <td><img src="https://teaching-h2020.eu/sites/default/files/styles/mt_brands/public/2020-02/Thales_logo.jpg" height="80"></td>
  <td><img src="https://teaching-h2020.eu/sites/default/files/styles/mt_brands/public/2018-06/itml400.png" height="80"></td>

  </tr>
  <tr >
  <td><img src="https://teaching-h2020.eu/sites/default/files/styles/mt_brands/public/2020-02/infineon_logo_rgb.jpg" height="80"></td>
  <td></td>
  <td></td>

  </tr>
</table>











## Fundings
<img src="https://teaching-h2020.eu/sites/default/files/inline-images/eu.jpg" height="50">


This project has received funding from the European Union’s Horizon 2020 Research and Innovation program under grant agreement No 871385.