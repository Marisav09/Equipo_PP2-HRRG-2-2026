# Página 1

**Equipo:** Monitor multiparametrico ePM

II

Preface

Manual Purpose

This manual provides detailed information about the assembling, dissembling, testing and

troubleshooting of the equipment to support effective troubleshooting and repair. It is not intended to be

a comprehensive, in-depth explanation of the product architecture or technical implementation.

Observance of the manual is a prerequisite for proper equipment maintenance and prevents equipment

damage and personnel injury.

Intended Audience

This manual is for biomedical engineers, authorized technicians or service representatives responsible for

troubleshooting, repairing and maintaining the monitors.

Passwords

A password may be required to access different modes. The passwords are listed below:

 User maintenance: 888888

 Manage Configuration: 315666

 Factory maintenance: 332888

 Demo mode: 2088

# Página 2

**Equipo:** Monitor multiparametrico ePM

1-1

1 Safety

1.1 Safety Information

WARNING

 Indicates a potential hazard or unsafe practice that, if not avoided, could result in death or

serious injury.

CAUTION

 Indicates a potential hazard or unsafe practice that, if not avoided, could result in minor

personal injury or product/property damage.

NOTE

 Provides application tips or other useful information to ensure that you get the most from your

product.

1.1.1 Warnings

WARNING

 This equipment is used for single patient at a time.

 This equipment and its accessories are suitable for use within the patient environment.

 To avoid explosion hazard, do not use the equipment in the presence of oxygen-rich

atmospheres, flammable anesthetics, or other flammable agents.

 Use and store the equipment in specified environmental condition. The monitor and

accessories may not meet the performance specification due to aging, stored or used outside

the specified temperature and humidity range.

 The equipment is not intended to be used within the Magnetic Resonance (MR) environment.

 Before connecting the equipment to the power line, check that the voltage and frequency

ratings of the power line are the same as those indicated on the equipment’s label or in this

manual.

 Before putting the system into operation, the operator must verify that the equipment,

connecting cables and accessories are in correct working order and operating condition.

# Página 3

**Equipo:** Monitor multiparametrico ePM

1-2

 To avoid risk of electric shock, the equipment must only be connected to mains power with

protective earth. If a protective earth conductor is not provided, operate it on battery power, if

possible.

 Do not use the multiple portable socket outlets (MPSO) or AC mains extension cords. Insure

that the sum of the individual ground leakage currents does not exceed the allowable limits.

 Do not touch the patient and live parts simultaneously. Otherwise patient injury may result.

 Do not come into contact with the patient during defibrillation. Otherwise serious injury or

death could result.

 Do not open the equipment housings. All servicing and future upgrades must be carried out by

trained and authorized personnel.

 Do not rely exclusively on the audible alarm system for patient monitoring. Turning the alarm

volume to a low level or off may result in a hazard to the patient. Remember that alarm

settings should be customized according to patient situations. Always keep the patient under

close surveillance.

 The physiological data and alarm messages displayed on the equipment are for reference only

and cannot be directly used for diagnostic interpretation.

 Route, wrap and secure the cables to avoid inadvertent disconnection, stumbling and

entanglement.

 The software equipment copyright is solely owned by Mindray. No organization or individual

shall resort to modifying, copying, or exchanging it or to any other infringement on it in any

form or by any means without due permission.

1.1.2 Cautions

CAUTION

 Use only parts and accessories specified in this manual.

 Ensure that the equipment is supplied with continuous electric power during work. Sudden

power failure may cause data loss.

 Magnetic and electrical fields are capable of interfering with the proper performance of the

equipment. For this reason make sure that all external devices operated in the vicinity of the

equipment comply with the relevant EMC requirements. Mobile phone, X-ray equipment or

MRI devices are a possible source of interference as they may emit higher levels of

electromagnetic radiation.

 Always install or carry the equipment properly to avoid damage caused by drop, impact,

strong vibration or other mechanical force.

 Dry the equipment immediately in case of rain or water spray.

 Some settings are password protected and can only be changed by authorized personnel.

Contact your department manager or biomedical engineering department for the passwords

used at your facility.

# Página 4

**Equipo:** Monitor multiparametrico ePM

1-3

 Dispose of the package material as per the applicable waste control regulations. Keep it out of

children’s reach.

 At the end of its service life, the equipment, as well as its accessories, must be disposed of in

compliance with the guidelines regulating the disposal of such products. If you have any

questions concerning disposal of the equipment, please contact us.

1.1.3 Notes

NOTE

 Put the equipment in a location where you can easily view and operate the equipment.

 The equipment use a mains plug as isolation means to the mains power. Do not locate the

equipment in a place difficult to operate the mains plug.

 The typical operator's position is in front of the monitor.

 The software was developed in compliance with IEC62304. The possibility of hazards arising

from software errors is minimized.

 This manual describes all features and options. Your equipment may not have all of them.

 Keep this manual in the vicinity of the equipment so that it can be obtained conveniently when

needed.

1.2 Equipment Symbols

See the  ePM Series Patient Monitor Operator’s Manual (P/N: 046-012606-00)  for information about the

symbols used on this product and its packaging.

# Página 5

**Equipo:** Monitor multiparametrico ePM

2-1

2 Product Principle

2.1 Overview

The ePM series multi-parameter monitors enable to provide complete patient management, adequate

physiological parameter monitoring and physiological alarm, possessing powerful data review function,

flexible wired or wireless network configuration and application ability. It provides a series of CAA

applications to assist physicians to make a diagnosis. Meanwhile, the ePM series provide hospital

management with superior monitor management applications to help hospitals to improve the efficiency

and quality of monitor equipment management.

Based on the needs of clinical applications, ePM series could provide product models with displays of

different sizes. Users can operate the monitor by touch screen or shortcut key.

The ePM series have good human-computer interaction design, clinical applicability, complete hospital IT

solution capabilities and lots of CDS applications.

2.2 Product System Structure

The ePM series monitors have only one main unit:

 ePM 10/ePM 10A/ePM 10C host uses 10.1" TFT WXGA display

 ePM 12/ePM 12A/ePM 12C host uses 12.1" TFT WXGA display

 ePM 15/ePM 15A/ePM 15C host uses 15.6" TFT WXGA display

 Both of them use a touch screen and shortcut buttons as input devices, with an optional remote

control

 Optional WiFi module

 Optional built-in recorder

# Página 6

**Equipo:** Monitor multiparametrico ePM

2-2

Main control/multi-parameter/ interface board

LCD/Touch Screen ON/OFF button board/ shortcut button board

Alarm indicator light board

AC-DC module Recorder (built-in, optional)

Speaker

AC-DC connector

2*USB VGA RJ45

WiFi module

Multi-purpose connector

Battery

Parameter module (built-in, optional)

Battery interface board DC_IN

Fig. 1- 1 System Block Diagram

2.2.1 Main Control Board/Parameter/Interface Board

The main control board includes the main control CPU, program memory, data memory, system

configuration memory, WiFi module (optional), power management MCU, charging circuit for batteries

and DC-DC circuit. A multi-parameter module circuit (ECG/Resp/SpO 2 /NIBP/IBP) is also integrated on this

board. In addition, there are internal and external interfaces. The internal interfaces include an interface for

the recorder, an internal parameter module interface, an interface between the AC-DC and the battery.

The external interfaces include a VGA display interface, a USB interface, an Ethernet interface and a

multi-function interface. (There is an additional DC_IN interface for ePM 10/ePM 10A/ePM 10C).

# Página 7

**Equipo:** Monitor multiparametrico ePM

2-3

Main processor

DDR3

Program memory

Data memory

E2ROM

USB hub

Touch screen controller SPI

US B

Audio codec/AMP Speaker

Touch Screen

Power M0

PHY

WiFi   optional  

Internal card cage backboard (for model M only)

RTC

Light sensor

Power button/power indicator light

RJ-45

VGA interface

USB 2*port

MMC

MMC

E2ROM

Alarm indicator light

LCD

Backlight drive

VGA transfer

SPI

UART LCDC

I2C

I2C

Main control/ parameter/ interface

RGB-LVDS

Multi-purpose connector

Parameter processor

Parameter acquisition circuit

UAR T UART/RS232

Nurse call/RS232

Analog Output

Parameter module(built-in)

Shortcut button

Fig. 1-2 Main Control Board Block Diagram

2.2.2 Power Supply Architecture

AC/DC module

100 ～ 240V AC AC-DC in

1 st  Battery

BAT charger

M0

DC/DC_1 +12V

DC/DC_ 2

LDO

+3.3V_1

VBUS ： 9.6 ～ 11.1V, +15V

ON/OFF

ON/OFF

+5V

Poweswitch board

+5V/+3.3V +3.3V

Alarm lamp board Photo senseor Led driver

Recorder

+12V

LCD&TP

+12V

Internal module rock COM board

+5V

ON/OFF

+3.3V

DC/DC

DC/DC 2 nd  Battery

BAT switch

DC_in 15V DC

Parameter module(integrated internally)

+12V

Isolation Power module

DC/DC _3

+1.325V

+1.35V +1.1V

+1.8V

+1.1V

+1.8V

+5V

Fig. 1-3 Power Supply Architecture Diagram

# Página 8

**Equipo:** Monitor multiparametrico ePM

2-4

The AC/DC power module outputs 15V to the main control board. By the internal DC-DC_2 and DC_DC_1

conversion circuits of the main control board, it can generate 3.3V, 5V and 12V to supply power for other

modules or boards in the host. The battery charging circuit is powered by 15V and can be switched

between AC power supply and battery power supply by AC connection test. The ePM12/ePM 12A/ePM

12C can support dual batteries. The first battery is installed in the main unit and the second battery is

installed in the external battery compartment. The external battery compartment is installed at the

bottom of the main unit. For the ePM15/ePM 15A/ePM 15C, the internal battery compartment can support

two batteries. The ePM Series monitors support 3 types of batteries, 2600mAh, 4500mAh and 5600mAh.

2600mAh and 4500mAh are interchangeable. 5600mAh cannot be used interchangeably with these two

batteries. The ePM 10/ePM 10A/ePM 10C can be mounted to an ambulance via a charging dock. There is

an isolated power module in the charging dock which converts the 28~12V input to a 15V output. The

output of the charging dock is connected to the DC_in interface of the ePM 10/ePM 10A/ePM 10C.

+12V is the power supply for the integral module rack, recorder and parameter acquisition circuit. The

power module for parameter acquisition adopts the DC-DC isolation design. DC_DC_3 is used to power

the main processor.

2.2.3 Alarm Indicator Light Board

There are LED alarm indicator lights and light sensors (optional) on the board. The light sensors conduct

ambient light detection in order to adjust the brightness of LCD background light.

2.2.4 Power On/Off Button Board/Shortcut Button Board

For the power switches, indicator lights and shortcut buttons are integrated on one board.

2.3 Data Logic Flow

Data acquisition

Data forwarding

System application

Display and user interface

Data output

Data storage

Fig.2- 3 Data Flow Diagram

The monitoring parameters are collected and analyzed by the module and then forwarded to the system

software via an integral or external module rack. The system software displays waveforms, values and

alarms, meanwhile the data, alarms and values will also be stored in the internal data memory. It can also

be sent to a central station or other monitors via network (wired or wireless).

# Página 9

**Equipo:** Monitor multiparametrico ePM

2-5

2.4 Power On/Off Signal Flow Diagram

Normal power supply and power-on

If power button is turned on

Yes

No

Turn on the 12V power (power on infrared backboard/recorder/parameter module) Turn on the 5V/3.3V power (power on main control/USB port/display/touch screen)

Power supply management MO

Power ON/OFF chart

# Página 10

**Equipo:** Monitor multiparametrico ePM

2-6

Power supply management MO running process

Runs properly

Whether the Battery voltage is lower than the power-off voltage?

Whether the power Button is kept being pressed for more than 3s ？

No

Yes

Send a request for power- off to the main control

Whether the power-off request is received? No

Yes

Turn off the main power supply

Yes

No

Whether the power button is kept being pressed for more than 10s/waiting for more than 10s Yes

Power OFF process.

# Página 11

**Equipo:** Monitor multiparametrico ePM

3-1

3 Wireless LAN (WLAN) Installation

3.1 Introduction

This section describes how to install the Wireless LAN (WLAN) for Mindray patient monitor.

3.2 Network Deployment Process

If the hospital has established a WLAN, follow the installation process below:

Mindray Marketing Agency or Sales Staff

Mindray Headquarters

Mindray Acting Servant

A0 Providing network requirements

A1 Communication with hospitals on the intention to order

A2 Communication with hospitals on network requirements and require hospitals to set up and adjust accordingly

A3 On-site adjustment

Pass/Fail

Pass

A4 Conclusion of a contract

A5 Device installation and commissioning

Fig. 3-1 Network deployment flow chart

# Página 12

**Equipo:** Monitor multiparametrico ePM

3-2

3.2.1 Output List

Operation Output Acceptance Criteria Template

A0 Wireless network requirements

for Mindray patient monitor

Determine the wireless network

deployment requirements for the

Mindray patient monitor.

Wireless network

requirement table

A3 Network inspection and

acceptance report

Confirm whether the customer

network meets the requirements of

the Mindray patient monitor by

questionnaires and measurements.

Wireless network

inspection and

acceptance table

A5 Installation confirmation

report

Confirm the actual operation of the

Mindray patient monitor after

installation.

Installation

confirmation table for

patient monitor

If the hospital plans to create a new WLAN for the Mindray patient monitor, make sure there is at least one

WiFi channel that is not in use. Otherwise, after establishing a new WLAN, it is impossible to meet the

requirements of the Mindray patient monitor in terms of co-channel interference. See the installation

process below:

Mindray Marketing Agency or Sales Staff

Mindray Headquarters

Mindray Acting Servant

A0 Providing network requirements

A1 Communication with hospitals on the intention to order

A2 Site survey and network design

A3 Conclusion of a contract

A4 Network installation

A5 Device installation and commissioning

Fig. 3-2 New WLAN installation process

# Página 13

**Equipo:** Monitor multiparametrico ePM

3-3

Operation Output Acceptance Criteria Template

A0 Wireless network

requirements for

Mindray patient

monitor

Determine the wireless network

deployment requirements for the

Mindray patient monitor.

Wireless network

requirement table

A2 Network design

document, list of

materials

/ /

A5 Installation

confirmation report

Confirm the actual operation of the

Mindray patient monitor after installation.

Installation confirmation

table for patient monitor

Precautions

 Network design and deployment engineering are complex and need a professional IT engineer

to help get the job done. This document does not contain these contents.

3.3 Network Requirements

The wireless network needs to meet the following requirements.

Table 3-1 Wireless network requirement table

No. Item Specific requirements

Wireless coverage requirements

1 WiFi coverage signal

strength (RSSI)

-65dBm

RSSI is the value displayed on the patient monitor

2 Co-channel interference 20dB (co-channel interference AP signal is at least 20dB lower

than the AP signal used by the monitor)

3 Ping

latency

The average latency of a PC or mobile phone is less than 100

milliseconds and the packet loss rate should be lower than 1%.

AP capability requirements

1 AP capability The expected number of devices connected to an AP must be

less than 50% of the AP capacity. For example, within the

coverage of an AP, usually there are 16 devices connected to the

AP, so the entitled number of devices that are allowed to be

connected to the AP at the same time must be greater than 32.

An AP can create multiple SSIDs.

2 Equipment density The maximum number of devices that can be connected to an

AP at the same time is 16.

(including patient monitors and other equipment).

WLAN features

# Página 14

**Equipo:** Monitor multiparametrico ePM

3-4

No. Item Specific requirements

1 AP channel width Set the AP channel width to 20MHz. Do not use the HT40 or

HT80.

2 802.11 protocol The WLAN cannot use protocols that are not supported by the

Mindray patient monitor, such as 802.11ac

3 Security mode The WLAN cannot use the security mode that is not supported by

the Mindray patient monitor.

WPA2-PSK is highly recommended. WPA2-Enterprise may

increase the off-line probability while roaming, so it is not

recommended.

4 Virtual local area

network for special use

(VLAN)

The patient monitor requires a special VLAN.

The use of VLAN can minimize the broadcast or multicast data

that may affect the stability of patient monitor.

Key settings

1 DHCP The DHCP server needs to keep a sufficient number of IP

addresses to ensure that the patient monitor can obtain an IP

address.

2 IGMP snooping Enable IGMP snooping if the patient monitor adopts multicast

3 Multicast If the patient monitor adopts multicast, the network multicast

function should be enabled.

4 Beacon and DTIM AP DTIM = 1, Beacon = 100 milliseconds

5 Service port See the Mindray Patient Monitor Network White Paper; require

network devices to turn on certain TCP/UDP ports for patient

monitors

3.4 Network Inspection and Acceptance

3.4.1 Tools and Resources

 A laptop with Windows 7 (or a later version) and a wireless network card installed. It is recommended

that the laptop be equipped with an Intel Centrino wireless adapter. If your laptop is configured with

a different wireless adapter, make sure it has high precision.

 In terms of wireless network survey tools, it is recommended to use professional survey tools such as

Tamograph, Wirelessmon or other professional network survey tools.

 Professional network engineer.

Precautions

 Those who implement WiFi network surveys should have received good training on WiFi. If you

do not have a professional network engineer, please ask a third party for help.

# Página 15

**Equipo:** Monitor multiparametrico ePM

3-5

3.4.2 WiFi Signal Calibration

Before testing network coverage by the use of a wireless network survey tool that runs on a laptop, follow

the steps below to use the patient monitor to calibrate the RSSI of the wireless network survey tool.

1. Keep the patient monitor close to the wireless network survey tool. The distance between the patient

monitor and the wireless network survey tool should not exceed 30cm and the distance from a

human body should exceed 50cm.

2. Simultaneously move the patient monitor and wireless network survey tool (keep the same distance

as before).

3. When the patient monitor displays the following RSSI values: -50dBm, -60dBm, -70dBm, and -80dBm,

record the RSSI value read by the wireless network survey tool.

4. When conducting a site survey, calibrate the RSSI of the wireless network survey tool relative to the

patient monitor (the RSSI of the patient monitor is the judge criterion for wireless coverage).

3.4.3 Network Inspection and Acceptance Process

This is done in two ways: First, complete the project that requires the hospital IT department to conduct

self-test, as shown in the network inspection and acceptance table. Then, the customer service personnel

or authorized party will conduct site test and confirm the remaining contents, and finally fill in the

network inspection and acceptance table. If any items are found to be non-conformed during the network

inspection and acceptance, adjust them before installing the patient monitor.

During the testing, need to enable the WiFi network SSID broadcast to ensure that the SSID of the WiFi can

be scanned.

Table 3-2 Wireless network inspection and acceptance table

No. Item Specific requirements Inspection and acceptance

method

Inspection results

Wireless coverage requirements

1 Received

signal

strength(RSSI)

≥ -65dBm

RSSI is the value

displayed on the patient

monitor

Service personnel use the

network survey tool to

perform tests.

Be sure to test all expected

coverage areas (such as

wards, corridors, toilets, stairs

and elevators).

2 Co-channel

interference

-20dB Service personnel use the

network survey tool to

perform tests.

Be sure to test all expected

coverage areas (such as

wards, corridors, toilets, stairs

and elevators).

# Página 16

**Equipo:** Monitor multiparametrico ePM

3-6

No. Item Specific requirements Inspection and acceptance

method

Inspection results

3 Ping

latency

The average latency of a

PC or mobile phone

using a normal WiFi

module is less than 100

milliseconds and the

packet loss rate should

be lower than 1%.

Steps for the service

personnel to perform the test:

1. Connect your PC or mobile

phone to the AP.

2. Connect another PC to the

LAN port to which the central

monitoring system is

connected.

3. Run the "ping –t –l 32 –w

1000 IPaddress-of -cellphone"

command for 10 minutes.

4. Run "ctrl+c".

AP capacity requirements

1 AP capability The expected number

of devices connected to

an AP must be less than

50% of the AP capacity.

For example, within the

coverage of an AP,

usually there are 16

devices connected to

the AP, so the entitled

number of devices that

are allowed to be

connected to the AP at

the same time must be

greater than 32.

An AP can create

multiple SSIDs.

Service personnel obtain the

AP model number from

hospital personnel or by

direct observation. Obtain an

AP data manual as per this

model number to confirm

related AP capabilities.

2 Equipment

density

The maximum number

of devices that can be

connected to an AP at

the same time is 12

(including patient

monitors and other

devices).

Check together with hospital

IT personnel to confirm

whether this requirement is

met.

WLAN features

1 AP channel

width

Set the channel width to

20MHz. Do not use the

HT40 or HT80.

Check together with hospital

IT personnel to confirm

whether this requirement is

met.

# Página 17

**Equipo:** Monitor multiparametrico ePM

3-7

No. Item Specific requirements Inspection and acceptance

method

Inspection results

2 802.11

protocol

The WLAN cannot use

protocols that are not

supported by the

Mindray patient

monitor, such as

802.11ac

Check together with hospital

IT personnel to confirm

whether this requirement is

met.

3 Security mode The WLAN cannot use

the security mode that

is not supported by the

Mindray patient

monitor.

WPA2-PSK is highly

recommended.

WPA2-Enterprise may

increase the off-line

probability while

roaming, so it is not

recommended.

Check together with hospital

IT personnel to confirm

whether this requirement is

met.

4 Virtual local

area network

for special use

(VLAN)

The patient monitor

requires a special VLAN.

The use of VLAN can

minimize the broadcast

or multicast data that

may affect the stability

of patient monitor.

Check together with hospital

IT personnel to confirm

whether this requirement is

met.

Key settings

1 DHCP The DHCP server needs

to keep a sufficient

number of IP addresses

to ensure that the

patient monitor can

obtain an IP address.

Check together with hospital

IT personnel to confirm

whether this requirement is

met.

2 IGMP snooping Enable IGMP

snooping if the

patient monitor

adopts multicast

Check together with hospital

IT personnel to confirm

whether this requirement is

met.

3 Multicast If the patient monitor

adopts multicast, the

network multicast

function should be

enabled.

Check together with hospital

IT personnel to confirm

whether this requirement is

met.

4 Beacon and AP DTIM = 1, Beacon = Check together with hospital

# Página 18

**Equipo:** Monitor multiparametrico ePM

3-8

No. Item Specific requirements Inspection and acceptance

method

Inspection results

DTIM 100 milliseconds IT personnel to confirm

whether this requirement is

met.

5 Service port See the Mindray Patient

Monitor Network White

Paper; need to keep

certain TCP/UDP ports

open for patient

monitors

Check together with hospital

IT personnel to confirm

whether this requirement is

met.

3.5 Use Patient Monitors to Assess Network Coverage

To confirm the coverage, perform a coverage test in the areas where patients often go around.

Confirm whether the coverage meets the requirements by observing the signal strength (RSSI) displayed

on the patient monitor and whether an off-line event occurs.

If necessary, adjust the AP position or increase APs to ensure adequate coverage.

Please follow the steps below:

1.  Set the patient monitor to access the central monitoring system.

2.  Perform a Ping command on the patient monitor via the central monitoring system (enter "ping – t – l

32 – w 1500 IP address" in the CLI window) (continue to run the Ping command on the patient

monitor. The data packet is 32 bytes and the reply timeout is 1500 milliseconds). Ten minutes later,

enter "ctrl + c" (complete Ping) to ensure that the average latency is less than 250 milliseconds and

the packet loss rate should be lower than 1%.

3.  Hold the patient monitor by hand and avoid being held up by other people. Walk around the

expected coverage areas (such as wards, toilets, smoking areas, corridors, and all corners of the

elevator).

4.  The number of disconnections from the central station should be less than 10% of the roaming times

of the patient monitor, and the RSSI value displayed on the patient monitor should not be lower than

-65dBm.

5.  If the signal strength is below -65dBm while walking around, stop walking at that location and

observe for 30 seconds. If the RSSI value is not lower than -65dBm for more than 66% of the time,

then it meets the coverage requirements.

# Página 19

**Equipo:** Monitor multiparametrico ePM

3-9

Table 3-3 Installation confirmation table for patient monitor

Testing or observing items Results (pass, fail or not applicable)

Perform a Ping command on the patient monitor via the central

monitoring system and ensure that the average latency is less than

250 milliseconds and the packet loss rate should be lower than 1%.

Hold the patient monitor by hand and walk around different AP

coverage areas. After walking around all the expected coverage areas,

observe the continuous waveforms on the central monitoring system.

The off-line time should be less than 10% of the patient monitor’s

roaming time.

In the position of worst coverage, the signal strength displayed on

the screen is higher than -65dBm.

Precautions

 If the monitor is assessed only for use in a fixed position instead of roaming among various

APs, then it’s unnecessary to walk around coverage area during testing. It is only necessary to

place the monitor at the possible installation position of the worst signal, and then confirm the

signal strength and Ping effect.

3.6 Recommended Network Equipment

The Cisco devices listed in the table below are recommended.

Device Parts No.

2500 wireless controller AIR-CT2504-x-K9

2600 wireless APs AIR-CAP2602I-x-K9

3.7 Seting the Wireless Parameters of the Patient Monitor

Configure the patient monitor's WLAN parameters as per the table below:

Parameters Settings recommended Remarks

[Main Menu]  →  [Maintenance]  →  [User Maintenance]  →  [Network Setup]  →  [WLAN]

SSID Set the actual network

name to be used

/

Security mode WPA2-PSK The security mode should be the same as that of the

WLAN deployed for the patient monitor.

If you are using EAP, choose the security mode based

on your WLAN deployment.

Password Set the actual network

password to be used.

/

[Main Menu]  →  [Maintenance]  →  [User Maintenance]  →  [Network Setup]  →  [WLAN] →  [WLAN Setup]

# Página 20

**Equipo:** Monitor multiparametrico ePM

3-10

Parameters Settings recommended Remarks

WLAN frequency band 5G The options include: 2.4G, 5G and Auto.

2.4G = use only 2.4GHz band

5G = use only 5GHz band

Auto = use 2.4GHz and 5G  Hz bands (5GHz shall

prioritize)

ID verification server

type

ACS Options include: ACS and SBR.

ACS refers to the Cisco access control server.

SBR refers to other servers except ACS.

It applies only when the security type is Enterprise.

BG channel Designate The options include: All, Designate and None.

Stability and roaming performance can be improved

by limiting the number of channels that the monitor

can be connected to. For example, on a 2.4GHz

network, set the channels to 1, 6, and 11, then the

network card will not scan or connect to other

channels.

The BG channel settings on the patient monitor must

match the AP channel settings.

Channel A Designate The options include: All, Designate and None.

Stability and roaming performance can be improved

by limiting the number of channels that the monitor

can be connected to.

The 5GHz channel settings on the patient monitor

must match the WLAN AP channel settings.

[Main Menu]  →  [Maintenance]  →  [User Maintenance]  →  [Network Setup]  →  [WLAN]  →  [Certificate

Management]

Local / Display the existing EAP certificate in patient monitor

USB driver / Display the existing EAP certificate in the USB driver

[Main Menu]  →  [Maintenance]  →  [Factory Maintenance]  →  [Setup]  →  [WLAN Setup]

Adjustment area International area South Korea, Turkey, Russia and Brazil need to be

configured separately. Other countries/regions only

need to choose international area.

The patient monitor needs to be restarted for the

patient monitor settings to take effect.

CCX features Support This means it supports CCX 4.0 and fast roaming

PMK cache Criteria The options include: Standard and OPMK.

The option of Standard refers to PMK cache.

OPMK refers to random key cache.

Trigger -70 When the RSSI is below the roam trigger value, the

network card will attempt to roam.

Scan cycle 5 When the RSSI is below the roam trigger value, the

probe request cycle is 5 seconds.

# Página 21

**Equipo:** Monitor multiparametrico ePM

3-11

The security modes supported by the monitor include:

menu

Basic

algorithm

Authentication

mode

Encryption

mode

Whether support CCKM

WPA PSK WPA PSK TKIP/RC4 No

WPA2 PSK WPA2 PSK CCMP/AES No

WPA PSK AES WPA PSK CCMP/AES No

WPA TKIP WPA EAP TKIP/RC4 No

WPA2 AES WPA2 EAP CCMP/AES No

WPA AES WPA EAP CCMP/AES No

CCKM TKIP CCKM EAP TKIP/RC4 Yes

CCKM AES CCKM EAP CCMP/AES Yes

After the EAP authentication mode is selected, the system will display corresponding configuration items.

The table below lists the configuration items for different EAP methods.

Identity Anonymous Password CA

certificate

User

certificate

PAC

certificate

PAC

Password

PEAP-MSCHAPV2 Y O Y Y N N N

PEAP-GTC Y O Y Y N N N

PEAP-TLS Y O Y Y Y N N

TTLS Y O Y Y N N N

TLS Y N Y Y Y N N

FAST Y O Y N N Y Y

LEAP Y N Y N N N N

Remarks: Y means "yes", N means "no", and O means "optional".

The meaning of each configuration item is shown below:

 Identity Verification Protocol (Phase 2 Identity Verification): When PEAP in the EAP method is selected,

the user can configure the following PEAP internal methods: EAP-MSCHAPV2, EAP-GTC and EAP-TLS.

 Identity: user identity, i.e. the user name in AD, LDAP, or local user management of the RADIUS server.

 Anonymous: This item does not affect the identity verification process. The function of this item is to

hide the real name (identity).

 Password: the password for the identity.

 CA certificate: Select the CA certificate from the imported certificates.

 User certificate: Select the user certificate from the imported certificates.

 PAC certificate: When EAP-FAST is selected, also select the PAC certificate from the imported

certificates. If the RADIUS server supports intra-band PAC deployment and deploy PAC for customers,

there is no need to set a PAC certificate or password.

 PAC password: Enter the PAC password for the PAC certificate when EAP-FAST is selected. If the

RADIUS server supports intra-band PAC deployment and deploy PAC for customers, there is no need

to set a PAC certificate or password.

# Página 22

**Equipo:** Monitor multiparametrico ePM

3-12

3.8 Troubleshooting

Sign Possible causes Recommended measures

The patient monitor

cannot be

connected to the

AP and an X is

displayed on the

patient monitor's

WiFi signal icon.

The nearby AP is not turned on. Make sure the AP is turned on and it belongs to the

VLAN for the patient monitor.

The patient monitor is not turned

on within the AP coverage area.

Go to the AP coverage area and turn on the patient

monitor. Ensure that the signal strength displayed

on the patient monitor is greater than –65dBm.

Ensure the co-channel interference meets the

requirements.

The SSID and IP address

acquisition mode and security

mode are not properly

configured on the patient

monitor.

Refer to this manual to reconfigure this

information.

Patient monitor fault. Check if another patient monitor can get online. If

possible, restart the patient monitor and make sure

the two patient monitors have the same

configuration. If the patient monitor is still unable

to get online then return it to Mindray for repair.

The patient monitor

can access AP but is

unable to be

connected to the

central monitoring

system.

The patient monitor is not

licensed to access the central

monitoring system.

Patient monitor is allowed to access the central

monitoring system.

The patient monitor is unable to

obtain any IP addresses, and the

IP addresses in the IP address

pool have all been taken.

Use other network devices to connect to the

central monitoring system and check if the IP

address can be obtained.

If the problem still exists, contact IT department.

A static IP address conflict has

occurred.

Observe if a prompt indicating an IP address

conflict is displayed on the patient monitor.

If this prompt is displayed, ensure that all network

devices have unique IP addresses.

Network link trouble. Confirm if the PC or mobile phone can ping the

central monitoring system after being connected

to the AP.

If the problem still exists, contact IT department.

The service port required for the

patient monitor is not enabled

on the hospital network.

Check if the service port required for the patient

monitor is enabled on the hospital network. If not,

enable related services (such as some UDP ports

and multicast).

If the problem still exists, contact IT department.

Intermittent

disconnection

occurs to a single

Move the patient monitor to the

blind coverage area.

Check if the WiFi signal strength is greater than

–65dBm in the location where disconnection

occurs.

# Página 23

**Equipo:** Monitor multiparametrico ePM

3-13

Sign Possible causes Recommended measures

patient monitor Patient monitor fault. Check if disconnection occurs easily to the patient

monitor at the same location. If the problem

cannot be resolved after restarting the patient

monitor, return the patient monitor to Mindray for

repair.

A static IP address conflict has

occurred.

Observe if a prompt indicating an IP address

conflict is displayed on the patient monitor.

Check if an IP address has been assigned to

multiple devices.

Intermittent

disconnection

occurs to multiple

patient monitors

APs in some areas are destroyed. Make sure the AP has been turned on and works

properly.

There is strong interference in

some areas.

Use the network survey tool to see if the

interference is strong and remove significant

sources of interference or adjust the WLAN

deployment to meet Mindray requirements.

Insufficient signal coverage in

some areas.

Use the network survey tool to check signal

coverage. If the signal coverage is insufficient in a

certain area, adjust the AP position or increase APs.

Intermittent

disconnection

occurs to all patient

monitors

Improper wired network

configuration

Use a wired patient monitor to check wired

network configuration Ensure that the WLAN

bandwidth configured on the switch is sufficient

with a 50% surplus

Radio interference exists Use the network survey tool to check if there is

radio interference and remove obvious sources of

interference or adjust the WLAN deployment to

meet Mindray requirements.

# Página 24

**Equipo:** Monitor multiparametrico ePM

4-1

4 Testing and Maintenance

4.1 Introduction

Service personnel need to inspect, maintain and test the monitor regularly to ensure that it can keep

working stably for a long time. This chapter provides basic test methods for the monitor as well as

recommended appropriate testing frequency and testing tools. Please maintain and test the monitor with

proper testing tools and according to actual needs.

The testing and inspection methods provided in this chapter are mainly used to confirm if the performance

of the monitor can meet the specifications. During the testing, if test results do not meet the requirements, it

indicates that the monitor or a certain function module of the monitor goes wrong and needs to be repaired

or replaced immediately. Any other questions, please contact our after-sales service department.

Attention

 All tests can only be performed by qualified professional service personnel.

 Be careful when setting up and changing the contents in the maintenance and

configuration menus, otherwise a data loss may be caused.

 Before the testing, service personnel need to ensure proper test tools and connection

lines are used. Service personnel should be able to use these test tools proficiently.

4.1.1 Test Device

See the following testing sections.

4.1.2 Test Report

After our service personnel have done the test, please record the details according to the maintenance

and testing report at the last page of this chapter and return it to the after-sales service department of the

company.

4.1.3 Preventive Maintenance

A list of items requiring preventive maintenance for this monitor is provided below. Regular maintenance

is recommended to be conducted at least once every two years (once a year for the CO 2  module). (See the

following sections for detailed testing procedures and contents)

Visual inspection

NIBP test

CO 2  testing and calibration

# Página 25

**Equipo:** Monitor multiparametrico ePM

4-2

4.1.4 Recommended Frequency

Inspection/maintenance items Recommended frequency

Preventive maintenance

Visual inspection Installation for the first time, or after each re-installation.

NIBP test

Pressure Test

1. When the user suspects that the measured value is not

accurate.

2. After repairing or replacing the relevant module.

3. At least once every 2 years for the NIBP module, and once

a year for the CO 2  module.

Leakage Test

Overpressure

protection circuit

test

Sidestream and

microstream CO 2

test

Leakage Test

Performance test

Module calibration

Performance test

ECG test

Performance test

1. When the user suspects that the measured value is not

accurate.

2. After repairing or replacing the relevant module.

3. At least once every two years At least once a year for CO 2

module.

Module calibration

Resp performance test

Spo 2  test

NIBP test

Pressure Test

Leakage Test

Temp test

IBP test

Performance test

Pressure calibration

C.O. test

Mainstream CO 2  test

Sidestream,

microstream CO 2

test

Leakage Test

Performance test

Module calibration

Nurse call test When the user suspects that the nurse call or analog output

function is not normal. Analog output test

Electric safety test

Electric safety test

Housing leakage

current test

1. After repairing or replacing the power module.

2. Or after the monitor falls off.

3. At least once every two years or as needed.

Earth leakage

current

Patient leakage

current

Patient auxiliary

current

Other tests

Power On test

1. Installation for the first time, or after each re-installation.

2. After repairing or replacing the parts of the main unit.

# Página 26

**Equipo:** Monitor multiparametrico ePM

4-3

Recorder check After repairing or replacing the recorder.

Network printing check

1. Installation for the first time.

2. After repairing or replacing the printer.

Battery check

Function check

1. Installation for the first time.

2. After replacing the battery.

Performance check

Every two months or when the battery running hours are

significantly shortened.

4.2 Preventive Maintenance

4.2.1 Visual Inspection

Visual check mainly refers to a comprehensive visual check on the monitor appearance. If the monitor has

no obvious physical damage, then it passes the visual check. The specific check items are as follows:

 Check if there’s physical damage to the monitor housing, display and buttons.

 Whether the module suffers physical damage.

 Whether the power cord, bracket and module accessories suffer physical damage.

 Whether the external cable wears out, whether the connector pin is loose or twisted.

 Whether the monitor’s peripheral interface is loose, whether the pins are twisted.

 Whether the safety label and nameplate are clearly legible.

4.2.2 NIBP Test

Pressure check

Test tools:

 T connector

 Airway tube

 Spherical air pump

 Rigid container: 500 ± 25 ml

 Standard pressure meter: has been calibrated with a precision of at least 1 mmHg

See the below for check steps:

1.  Connect the monitor, standard pressure meter, spherical air pump and rigid container as shown

below.

# Página 27

**Equipo:** Monitor multiparametrico ePM

4-4

```metadata
pagina: 27
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P27_I0.png
contexto: 
```

![Imagen página 27 - 0](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P27_I0.png)

2.  The standard pressure meter’s reading should be zero before air inflation. If it is not zero, open the

spherical air pump valve so that the airway leads to the atmosphere until the standard pressure

meter reads zero, then close the valve.

3.  Select [ Main Menu ] → [ Maintenance ] → enter password → [ Module ] → [ NIBP ] → [ NIBP Pressure

Test ].

4.  Check the readings of the standard pressure meter and the monitor, both of which should show a

pressure value of 0mmHg.

5.  Inflate the rigid container with a spherical air pump until the internal pressure reaches 50mmHg, then

stop inflating and wait for 10s in order that the measurement value keeps stable.

6.  Check the readings of the standard pressure meter and the monitor. The difference between the two

should be within 3mmHg. If the difference is greater than 3mmHg, please contact service personnel.

7.  Inflate the rigid container with a spherical air pump until the internal pressure reaches 200mmHg,

then stop inflating and wait for 10s in order that the measurement value keeps stable. Repeat step 6.

Precautions

 You can also use a blood pressure simulator instead of a spherical air pump and a standard

pressure meter to form a test system.

 You can also replace the rigid container with cylinders and cuffs of a right size.

Leakage Test

Testing tools:

 Adult cuff

 Airway tube

 Cylinder

See the below for testing steps:

1.  Set [ Patient Category ] to [ Adult ].

2.  Connect well the cuff with the NIBP cuff connector of the monitor.

3.  Wrap the cuff around a cylinder of a right size, as shown in the figure.

Monitor

NIBP cuff connector

Pressure meter

Airway tube

Spherical air pump Rigid container

# Página 28

**Equipo:** Monitor multiparametrico ePM

4-5

```metadata
pagina: 28
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P28_I0.png
contexto: 
```

![Imagen página 28 - 0](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P28_I0.png)

4.  Select [ Main Menu ] → [ Maintenance ] → enter password → [ Module ] → [ NIBP ] → [ NIBP Leakage

Test ], the NIBP parameter area will display [ Leakage Test... ].

5.  After approximately 20 seconds, the system will automatically deflate which indicates the leakage

test is completed.

6.  If there is no prompt message in the NIBP parameter area, it means there is no air leakage in the

system. If [ NIBP Air Leakage ] is displayed, it indicates that there may be an air leakage. At this time,

the operator should check whether there is loose connection, whether the cuff and the inflation tube

are damaged or leaked. When the connection is confirmed to be proper and there’s no leakage in the

cuff or the airway tube, then conduct a leakage test once again.

You can also perform a leakage test manually:

1.  Perform steps 1 to 4 in the Pressure Calibration section.

2.  Inflate the metal container with a spherical air pump until the internal pressure reaches 250mmHg,

then stop inflating and wait for 5s in order that the measurement value keeps stable.

3.  Record the current pressure and start timing using a timer. Record the pressure value after 60s.

4.  The displayed pressure value after 60s minus the pressure value displayed at the beginning of the

leakage test should not exceed 6mmHg.

Overpressure protection circuit test

Testing tools:

 T connector

 Airway tube

 Spherical air pump

 Rigid container: 500 ± 25 ml

 Standard pressure meter: has been calibrated with a precision of at least 1 mmHg

1.  Perform steps 1 through 4 in the NIBP Pressure Check section.

2.  Select [ Main Menu ]  → [ Maintenance ] → enter password → [ Factory Maintenance ] → [ NIBP ] →

[ Test ].

3.  In [ Overpressure Protection Circuit Test ], select [ Adult/Child ] for [ Patient Category ], adjust the

output pressure of the air pump to 320-330mmHg. After it keeps stable, select the [ Test ] button to

Monitor

NIBP cuff connector

Inflation tube

Cylinder

Cuff

# Página 29

**Equipo:** Monitor multiparametrico ePM

4-6

start  calibration . When the  test  succeeds, the NIBP menu will display the prompt of [ Test  Successful].

If the pressure exceeds 320-330mmHg, [ Test  Failed] will be displayed.

4. In [ Overpressure Protection Circuit Test ], select [ Neo ] for [ Patient Category ] and adjust the air

pump output pressure to 160-165mmHg. When the value keeps stable, select the [ Test ] button on

the right side of the menu to start  Test . When the  test  succeeds, the NIBP menu will display the

prompt of [ Test Successful ]. If the pressure exceeds 160-165mmHg, [ Test Failed ] will be displayed.

4.2.3 Sidestream and Microstream CO 2  Testing and Calibration

Leakage Test

1. After the CO 2  preheating startup is completed, block the module or the water tank inlet hole

completely by hand or other objects, the sidestream and microstream CO 2  modules will have

different actions respectively:

 Sidestream: Plug the sidestream CO 2  module into the module rack of the main unit. Wait for

1min., after the module completes preheating startup, block the module air intake with your

fingers or other objects. The monitor will display the alarm message of [ CO 2 Airway Occluded ].

Keep blocking it for about 60s, check [ Maintenance ]  →  enter password  →  [ module ]  →  [ CO 2 ]  →

[ CO 2 Module Calibration ], check that the current flow rate of the module is <10ml/min, and the

alarm message continues, then it proves that the module has no air leakage. If the alarm

message of [ CO 2  Airway Occluded ] disappears or the current flow rate is ≥10ml/min, it indicates

that there is air leakage.

 Microstream: Keep blocking the module air intake for 3s, the screen displays the alarm message

of [ CO 2  Purging ]; continue to keep blocking it for about 30s, the alarm message of [ CO 2  Airway

Occluded ] is displayed, then it proves that the module has no air leakage.

Precision test

Test tools:

 A steel cylinder containing 6 ± 0.05% CO 2  and a balance gas of N 2 .

 Steel cylinder with O 2  gas (its concentration >40%) and a balance gas of N 2  (for sidestream CO 2

module with oxygen module)

 T connector

 Airway tube

 Flowmeter

1.  Insert the module into the module rack.

2.  After the CO 2  preheating startup is completed, check the airway and conduct leakage test to ensure

that there is leakage.

3.  Go to [ Maintenance ] → [ Module ] → [ CO 2 ] → [ CO 2 Module Calibration ].

4.  Connect the test system as shown below.

# Página 30

**Equipo:** Monitor multiparametrico ePM

4-7

```metadata
pagina: 30
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P30_I0.png
contexto: 
```

![Imagen página 30 - 0](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P30_I0.png)

5.  Open and adjust the pressure reducing valve switch until the flow rate indicated by the flowmeter is

10~50mL/min and it keeps stable.

6.  Check and ensure that the real-time concentration of CO 2  displayed in the calibration menu is

6 ± 0.2% (45 ± 2mmHg for microstream CO 2 ).

Module calibration

Test tools:

 A steel cylinder containing 6 ± 0.05% CO 2  and a balance gas of N 2

 T connector

 Airway tube

 Flowmeter

1.  Ensure that the sidestream CO 2  module or the microstream CO 2  module has completed preheating or

startup.

2.  Check the airway and conduct leakage test to ensure there is no leakage.

3.  Open the [ CO 2 Calibration ] menu: select [ Main Menu ] → [ Maintenance ] → enter the user

maintenance password →  [ Module ] → [ CO 2 ].

4.  Select [ Zero ] in the [ CO 2 ] menu.

5.  After it is successfully set to zero, connect it as shown below.

Monitor

Gas cylinder

Flowmeter

Pressure reducing valve

采样管

T connector

Sampling tube

# Página 31

**Equipo:** Monitor multiparametrico ePM

4-8

```metadata
pagina: 31
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P31_I0.png
contexto: 
```

![Imagen página 31 - 0](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P31_I0.png)

6.  Open and adjust the pressure reducing valve switch until the flow rate indicated by the flowmeter is

10~50mL/min and it keeps stable.

7.  Enter 6% (CO 2  concentration value) in the [ CO 2 %] text box of the [ CO 2 Calibration ] menu.

8.  The current measured CO 2  concentration will be displayed in the [ CO 2 Calibration ] menu. Wait until

the measured CO 2  concentration keeps stable, select [ Calibration ] to calibrate the CO 2  module.

After the calibration is successful, the [ Calibration Completed ] message will be displayed on the [ CO 2

Calibration ] menu; if the calibration fails, the [ Calibration Failed ] message will be displayed. In this case,

please check if the calibration operation is correct and re-calibrate. If multiple calibrations fail, please

return to the factory for repair.

4.3 Power On Test

The power-on test is conducted to confirm whether the monitor can be turned on and work properly. If

the monitor can be started as follows, then it passes the power-on test. Specific steps:

1.  Connect the monitor to an AC power. The AC power indicator lights up and the battery indicator light

is on.

2.  Press the power switch to turn on the monitor, the system will give a "beep" sound (indicating that

the alarm sound passes the self-test); the red, yellow and green alarm lights light up respectively, and

finally go out (indicating that the alarm lights pass the self-test)).

3.  The startup screen disappears and enters the main interface of the system, and the normal startup is

completed.

Monitor

Gas cylinder

Flowmeter

Pressure reducing valve

采样管

T connector

Sampling tube

# Página 32

**Equipo:** Monitor multiparametrico ePM

4-9

4.4 Module Performance Test

4.4.1 ECG Test

ECG performance test

Test tools:

 Patient simulator Medsim300B

1.  Connect the patient simulator to the ECG parameter module with the ECG lead wire.

2.  Set the simulators as follows: ECG sinus rhythm, HR = 60 bpm, amplitude is 1 mV.

3.  Check and ensure that the ECG waveform display is normal and with no noise, and the HR value

displayed on the monitor should not exceed 60 ± 1 bpm.

4.  Disconnect each lead in turn, and observe that the screen displays the corresponding lead-off

information.

5.  Set the output pace signal of the simulator, set the [ Pace ] to [ Yes ] for the monitor, and confirm that

the screen displays the pacing sign.

ECG calibration

Test tools:

 Vernier caliper

1.  Set the [ Filter Mode ] of ECG parameters to be [ Diagnose ].

2.  Select [ Main Menu ] → [ Maintenance ] → enter password → [ Module ].

3.  Select [ Calibration ], square wave signal will appear on the screen, and the technical alarm area will

display [ ECG is Calibrating ].

4.  Compare the amplitude of the square wave with the scale, and the error range should be no more

than 5%.

5.  After completing the calibration, select [ Stop Calibration ].

When needed, you can also output the above wave and scale by the recorder and measure the accurate

error.

4.4.2 Resp Test

Test tools:

 Patient simulator Medsim300B

1.  Connect the simulator and monitor with a non anti-ESU cable and set the monitor’s resp lead to II.

# Página 33

**Equipo:** Monitor multiparametrico ePM

4-10

2.  Simulator settings: set the resp lead to II; basic damping to 500 Ω; variable damping to 1 Ω; and resp

rate to 20 rpm.

3.  Check if the monitor displays the RESP waveform with no distortion and that the displayed Resp

value must not exceed 20 ± 1 rpm.

4.4.3 SpO 2  Test

Test tools:

 None

1.  Connect the adult SpO 2  sensor to the monitor SpO 2  interface, set the [ Patient Category ] of the

monitor to [ Adult ], and set [ PR Source ] to SpO 2 .

2.  Measure the SpO 2  of your finger (assuming you are in a healthy state).

3.  Check that the monitor displays the pleth waveform and PR value of blood oxygen, and the displayed

saturation value range of blood oxygen should be between 95%-100%.

4.  Remove the SpO 2  sensor from your finger and confirm that an alarm is given to indicate the SpO 2

sensor is off.

Confirmation of measurement accuracy:

The accuracy of the MPM SpO 2  module has been confirmed in human experiments by comparison with

the reference values of arterial blood sample measured by a CO-oximeter. The measurements of pulse

oximeter are statistically consistent, and it is expected that only about two-thirds of the measurements will

be within the specified accuracy compared to the measurements of CO-oximeter.

Precautions

 The simulator cannot be used to verify the accuracy of the oxygen saturation monitor or the

SpO 2  sensor, and can only prove that the working state of the monitor is normal. The accuracy

of the oxygen saturation monitor or SpO 2  sensor needs to be verified by clinical data.

4.4.4 NIBP Test

See  4.2.2 NIBP  test.

4.4.5 Temp Test

Test tools:

 Resistance box (accuracy not less than 0.1Ω)

1.  Use a wire to connect both ends of any individual temperature interface of the parameter module to

both ends of the variable resistor box.

2.  The resistance box is set to 1354.9 Ω (corresponding to a temperature value of 37°C),

# Página 34

**Equipo:** Monitor multiparametrico ePM

4-11

3.  Verify each temperature channel of the monitor, and ensure that the monitor’s display value does not

exceed 37 ± 0.1°C.

4.4.6 IBP Test

Performance test

Test tools:

 Patient simulator Medsim300B, MPS450 or other equivalent devices

 Adapter cable for IBP test (300B, P/N: 00-002199-00) (MPS450, P/N: 00-002198-00)

1.  Connect the simulator to the monitor’s IBP parameter module.

2.  Set that the simulator outputs 0mmHg to each IBP channel.

3.  Press the "Zero" button of IBP module to conduct zero calibration for the parameter module.

4.  Set the static pressure of the monitor = 200mmHg.

5.  The display value on the monitor should not exceed 200 ± 2mmHg

6.  If the error exceeds ± 2mmHg, perform a pressure calibration for the IBP parameter module. If the IBP

parameter module has been calibrated for pressure with a reusable IBP sensor connected, then

connect the IBP sensor and check the pressure calibration results.

7.  Set the simulator to output 120/80mmHg ART signal and 120/0mmHg LV signal to each IBP channel

respectively, and check if the IBP waveform is displayed correctly.

Pressure calibration

Method 1:

Test tools:

 Patient simulator Medsim300B, MPS450 or other equivalent devices

 Adapter cable for IBP test (300B, P/N: 00-002199-00) (MPS450, P/N: 00-002198-00)

1.  Connect the simulator to the monitor’s IBP parameter module.

2.  Set the simulator to zero pressure.

3.  Press the "Zero" button of IBP module to conduct zero calibration for the parameter module.

4.  Set the static pressure of the monitor = 200mmHg.

5.  Select [ Main Menu ] → [ Maintenance ] → enter the user maintenance password → [ Module ] →

[ IBP ] → [ Calibration ].

In the [ IBP ] menu, set the calibration value of the target pressure to 200mmHg.

6.  Select the [ Calibration ] button on the right side of the target channel and the monitor will begin

calibrating.

7.  When calibration completes, it will display [ Calibration Completed ]. If it cannot be calibrated, it will

display corresponding prompt message.

# Página 35

**Equipo:** Monitor multiparametrico ePM

4-12

Method 2:

Calibration tools:

 Pressure meter

 Spherical air pump

 Airway tube

 T connector

1.  Connect the three-way switch to the sphygmomanometer and the spherical air pump using a

T-connector, as shown below.

2.  First perform zero calibration. After the calibration is completed, the three-way switch leads to the

sphygmomanometer.

```metadata
pagina: 35
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P35_I0.png
contexto: 
```

![Imagen página 35 - 0](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P35_I0.png)

3.  Select [ Main Menu ]  →  [ Maintenance ]  →  enter the user maintenance password  →  [ Module ]  →  [ IBP ]

→  [ Calibration ]. In the open interface, set the target pressure calibration value of the target channel.

Input the range: 80 ~ 300mmHg.

4.  Inflate with a spherical air pump to allow the pressure reading of the sphygmomanometer to get

close to the pressure set in the menu.

5.  Repeat the adjustment of the calibration pressure value in the menu and the pressure value of the

sphygmomanometer until they are the same.

6.  Select the [ Calibration ] button of the target channel and the defibrillation monitor will begin

calibrating.

7.  When calibration completes, it will display [ Calibration Completed ]. If it cannot be calibrated, it will

display corresponding prompt message.

4.4.7 C.O. Test

Test tools:

 Patient simulator Medsim300B

 C.O. adapter box (for 300B)

Pressure sensor interface cable

IBP module

Sphygmomanometer

T-connector

Three-way switch

Pressure sensor

# Página 36

**Equipo:** Monitor multiparametrico ePM

4-13

1.  Connect the simulator to the monitor C.O. parameter module using the main cable of C.O. accessory.

2.  Set the simulator’s blood temperature (TB) to 37 °C and ensure that the display value on the monitor

does not exceed 37 ± 0.1 °C.

3.  Set the [ Injection Temp Source ] to [ Manual ], adjust the [ Injection Temp Value ] (TI) until it displays

24 °C, select [ C.O. Measure ], open the C.O. measure window, and set [ Comp Const ] to 0.595.

4.  Set the injection temperature of the C.O. simulator to 24 °C, and the cardiac output to 5 L/min. Press

[ Start ] in the C.O. measure window to start C.O. measure, then within 3 to 10s, press the RUN button

of the simulator.

5.  The displayed C.O. measure result is 5 ± 0.25L/min.

4.4.8 Mainstream CO 2  Test

Precautions

 Before performing the mainstream CO 2  test, check and ensure that the atmospheric pressure

setting in the [CO 2  Module Maintenance] of [Maintenance] is consistent with the local

atmospheric pressure value.

Test tools:

 A steel cylinder containing 6 ± 0.05% CO 2  and a balance gas of N 2 .

 Steel cylinder with 100% N 2  gas

 T connector

 Airway tube

 Flowmeter

1.  Insert the module into module rack and connect a sensor.

2.  When the CO 2  preheating startup completes, go to the [ CO 2 Setup ] menu, click [ Zero ] to conduct

zero calibration for the CO 2  module. If the zero calibration fails, the screen prompts [ Zero Failed ]; if

the zero calibration succeeds, the baseline of the CO 2  waveform on the screen returns to the zero

position.

3.  Go to [ CO 2  Setup ] menu and set [ Apnea Delay ] to 10s.

4.  Place the sensor in front of the mouth and breathe, so that the CO 2  waveform is generated on the

screen, then place the sensor in the air and ensure that the monitor generates an alarm message [ CO 2

Apnea ].

5.  Connect the test system as shown below.

# Página 37

**Equipo:** Monitor multiparametrico ePM

4-14

```metadata
pagina: 37
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P37_I0.png
contexto: 
```

![Imagen página 37 - 0](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P37_I0.png)

6.  Open the pressure reducing valve of the N2 cylinder and the CO 2  cylinder respectively, and ensure

that only one cylinder is connected to the T-connector at the same time.

7. Adjust the pressure reducing valve switch respectively so that the flow rate indicated by the flow

meter is 2~5L/min and it keeps stable.

8.  Switch the cylinder connected to the T-connector at an interval of 6s~10s and ensure that the CO 2

display value should be 45 ± 2mmHg.

4.4.9 Sidestream and Microstream CO 2  Testing and Calibration

See  4.2.3 Sidestream  and microstream CO 2  testing and calibration.

4.5 Nurse Call Test

Test tools:

 Multimeter

1.  Connect the nurse call line to the nurse call output port of the monitor.

2.  Set the monitor to [ Demo ] status, select [ Main Menu ] → [ Maintenance ] → enter the user

m aintenance password → [ Alarm ] → [Nurse Call].

3.  In the [ Nurse Call ] menu, select [ Alarm Priority ] and [ Alarm Category ], and set [ Trigger Mode ] to

[ Normally Open ].

4.  In the [ Nurse Call ] menu, set [ Signal Type ] to [ Pulse ]. Set the monitor to generate an alarm, check

the pulse with a pulse width of 1s when there is an alarm, and the multimeter measures the

conducting state.

CO 2  cylinder

Pressure reducing valve

T connector

N2 cylinder

Pressure reducing valve

T connector

Monitor

Mainstream sensor head

Flowmeter

# Página 38

**Equipo:** Monitor multiparametrico ePM

4-15

5.  In the [ Nurse Call ] menu, set [ Signal Type ] to [ Continuous ]. Set the monitor to generate an alarm,

check the continuous high level outputted when there is an alarm, and the multimeter can measure

the conducting state.

4.6 Analog Output Test

Test tools:

 Patient simulator

 Oscilloscope

1.  Connect the patient simulator to the monitor via an ECG line or IBP measurement line, and connect

the oscilloscope to the analog output port.

2.  Verify that the waveform displayed on the oscilloscope matches that displayed on the monitor

screen.

4.7 Electric Safety Test

Warning

 Electrical safety test is used to test the electrical safety of the monitor under test. It’s used to

detect abnormal electrical hazards. If these hazards are not detected in time, it may cause harm

to patients or operators.

 Electrical safety tests can be carried out using test equipment such as commercially available

safety analyzers. Service personnel are required to ensure the applicability, functional

integrity and safety of the test equipment, and familiarize with the use of it.

 Electrical safety test should comply with the following standards: EN 60601-1 and UL60601.

 If it’s stipulated otherwise by local laws and regulations, please carry out relevant electrical

safety tests in accordance with applicable regulations.

 In the patient area, all the equipment that uses AC power and is connected to medical

equipment must comply with IEC 60601-1 and must receive electrical safety test at the

intervals as required by the monitor.

Electrical safety test is used to detect electrical hazards that may cause harm to patients, operators and

service personnel. Perform electrical safety tests under normal conditions (including temperature,

humidity and atmospheric pressure).

The electrical safety test given in this chapter uses the 601 safety analyzer as an example. The safety analyzers

used may vary by different regions. Please ensure the applicability of your electrical safety test plan.

# Página 39

**Equipo:** Monitor multiparametrico ePM

4-16

See the figure below for equipment connection.

```metadata
pagina: 39
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P39_I0.png
contexto: 
```

![Imagen página 39 - 0](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P39_I0.png)

Module under test

A: AC power (programmable power supply, regulate frequency) B: Isolation figure for leakage current test on tooling C: Safety tester

Test tools:

 Safety analyzer

 Isolation transformer

4.7.1 Housing Leakage Current Test

1.  Connect the 601 safety analyzer to a 264 VAC, 60 Hz power supply.

2.  Connect the equipment under test to the auxiliary power output jack of the 601 safety analyzer via a

power line.

3.  Connect one end of the red test lead to the "Red input terminal" of the safety analyzer and press the

other end against the metal foil that is in close contact with the housing surface of the equipment

under test.

4.  Power on the 601 safety analyzer and press "5-Enclosure leakage" on the panel of the 601 safety

analyzer to enter the interface for housing leakage current test.

5.  Normally the leakage current of the housing is not more than 100 μA, and not more than 300 μA in a

single fault condition.

4.7.2 Earth Leakage Current Test

1.  Connect the 601 safety analyzer to a 264 VAC, 60 Hz power supply.

2.  Connect the application part of the equipment under test to the RA side of the safety analyzer.

3.  Connect the equipment under test to the auxiliary power output jack of the 601 safety analyzer via a

power line.

# Página 40

**Equipo:** Monitor multiparametrico ePM

4-17

4.  Power on the 601 safety analyzer and press "4-Earth leakage" on the panel of the 601 safety analyzer

to enter the interface for earth leakage current test.

5.  Normally the earth leakage current is not more than 300 μA, and not more than 1000 μA in a single

fault condition.

4.7.3 Patient Leakage Current Test

1.  Connect the 601 safety analyzer to a 264 VAC, 60 Hz power supply.

2.  Connect the application part of the equipment under test to the RA side of the safety analyzer.

3.  Connect the equipment under test to the auxiliary power output jack of the 601 safety analyzer via a

power line.

4.  Power on the 601 safety analyzer and press "6-Patient leakage" on the panel of the 601 safety

analyzer.

5.  Press the "APPLIED PART" button continuously to select AC and DC measurements. When it’s DC, "DC"

is displayed behind the limit value.

6.  Normally the patient leakage current is not more than 10 μA, and not more than 50 μA in a single

fault condition.

4.7.4 Patient Auxiliary Current Test

1.  Connect the 601 safety analyzer to a 264 VAC, 60 Hz power supply.

2.  Connect the equipment under test to the auxiliary power output jack of the 601 safety analyzer via a

power line.

3.  Connect the ECG line of the equipment under test to the RA end of the safety analyzer.

4.  Power on the 601 safety analyzer and press the "8-Patient Auxiliary Current Test" on the panel of the

601 safety analyzer to enter the interface for patient auxiliary current test.

5.  Press the "APPLIED PART" button continuously to select AC and DC measurements. When it’s DC, "DC"

is displayed behind the limit value.

6.  Normally the patient auxiliary current is not more than 10 μA, and not more than 50 μA in a single

fault condition.

4.8 Recorder Check

Test tools:

 None

1.  Print the ECG waveform, the recorder should be able to print normally with sound clarity and

consistency.

2.  Setup should ensure that relevant prompts should be displayed if it is out of paper or the buckle

cambers or other malfunctions, and it should work normally after recovery.

# Página 41

**Equipo:** Monitor multiparametrico ePM

4-18

3.  Perform alarm printing for each parameter, turn on the alarm recording switch of each parameter, set

different alarm limits, and ensure to conduct printing for each parameter alarm.

4.9 Network Printing Check

Test tools:

 Hub and network cable

4.9.1 Equipment Connection and Setup

1  Equipment connection: Connect the monitor and network printer to the hub via a common network

cable, as shown in the following figure:

2  IP setup: Go to the "Main Menu" interface, select [ Main Menu ] → [ Maintenance ] → enter the user

maintenance password, select [ Network Setup ] in the maintenance interface, and set the IP address

of the monitor to be in the same network segment with the IP address of the network printer (See the

instructions for the printer).

4.9.2 Printing Function Test

1  Enter demo mode of the monitor.

2  Go to the "Main Menu" interface, select [ Interface Setup ]  → [ Interface Layout ], and select "ECG

Full-Screen 7 Lead Interface".

3  Go to the "Main Menu" interface, select [ Normal Report ] → [ ECG Report ], select normal report, click

"Print", and the network printer should print out the ECG report.

4.10 Battery Check

Test tools:

 None

Monitor Network

printer

HUB

Network Cable

Network Cable

# Página 42

**Equipo:** Monitor multiparametrico ePM

4-19

Function check

1.  Check that the monitor works properly when powered by AC.

2. Remove the AC power line and check that the monitor continues to operate properly.

Performance check

Please refer to the relevant contents in the  battery  section of the operator’s manual to check that the

battery power supply time meets the specifications.

4.11 Charging Dock Check

Test tools:

 Multimeter

Function check

1.  Disconnect the charging dock from the monitor and connect the charging dock to the DC power

supply (12V-28) on the ambulance.

2.  When the charging dock is powered on, the green power indicator lights are lit.

3.  Use a multimeter to measure the output port voltage of the transmission dock. The voltage should be

(15V +5%).

4.  Connect the monitor and check if it can be turned on properly.

4.12 Factory Maintenance

4.12.1 Enter Factory Maintenance

Select [ Main Menu ] hot key  →  turn to the page 3  →  select [ Maintenance ] from the [ System ] column  →

enter the factory maintenance password  →  select [ Ok ], then select factory maintenance.

4.12.2 Monitor Iinformation (Exporting Log)

Before inserting the USB flash drive, confirm that its format is FAT32, and then insert it into the USB port of

the monitor’s main unit (Note: Not the USB port of the iView’s main unit!) ,

Open the [ Monitor Information ] menu, you can see the information about the monitor’s main unit, such

as: CPU temperature, Wifi signal strength, hard disk capacity and so on.

At this point, you can export all the monitor’s log information by clicking the "Export Log" button in the

bottom left corner of the window.

4.12.3 Production Test

Open the [ Production Test ] menu and you can perform basic function tests related to the monitor’s

hardware interface.

# Página 43

**Equipo:** Monitor multiparametrico ePM

4-20

Production test includes auto test and single test.

 Auto test: After selecting [ Start Auto Test ], the system will automatically completes all tests in order.

 Single test: Select one for a single test.

4.12.4 Setup

Open the [ Setup ] menu and you can do ECG alarm settings and other configurations.

4.12.5 Debugging

Open the [ Debug ] menu and you can make settings related to debugging tests.

4.12.6 Power Information

Open the [ Power Info ] menu and you can check the power status of the monitor.

4.12.7 Clinical Data

Open the [ Clinical Data ] menu and you can do settings related to clinical data collection.

When the Clinical Data Location is selected as "Local", the clinical data is stored in the monitor. You can

export the data to the USB flash drive by the same way as exporting the log.

When the Clinical Data Location is selected as "Udisk", the clinical data is directly stored in the U disk.

4.12.8 Sending Clinical Data

Open the Send Clinical Data menu and you can select the clinical data you need to send.

4.12.9 Software Version

Open the maintenance menu and select the [Version] menu, you can view all the software versions in the

system that can be viewed.

Maintenance test report

(For detailed test steps and contents, see the above section)

Client name

Client address

Maintenance people

Maintenance company name

Name of device under test

Model of device under test

Serial No. of device under test

Hardware version

Software Version

Test device Model/No. Validity of calibration

# Página 44

**Equipo:** Monitor multiparametrico ePM

4-21

Test Item Test result

Test result

(Pass/Fail)

Visual inspection

There should be no physical damage to the monitor housing,

display, buttons, SMR, modules, power cords, brackets and module

accessories

The external connection cable should be free of wear and the

connector pins should have no looseness or distortion

The monitor’s peripheral interface should have no looseness or

distorted pins

Safety labels and nameplates should be clearly legible

Power On test

It passes power-on test, the power indication and alarm system work

normally, and the monitor starts normally.

Performance test

ECG performance test

The ECG waveform is normal and noise-free, and the HR value

displayed on the monitor must not exceed 60 ± 1 bpm

The "ECG Lead Off" alarm works properly.

When the pacing is turned on, the pacing signal can be detected

and the pacing mark is displayed.

The difference between ECG calibrated waveform amplitude and

scale amplitude should not exceed 5%

RESP test

The monitor shows that the RESP waveform is not distorted, and the

displayed Resp value must not exceed 20 ± 1 rpm.

SpO 2  test

Connect healthy people’s finger to test, the monitor displays the

blood oxygen pleth waveform and the PR value, and the displayed

SpO 2  value range should be 95% to 100%.

SpO 2  sensor off alarm function is normal

NIBP test

For NIBP pressure test, 0, 50 and 200mmHg test difference does not

exceed ± 3mmHg

There is no gas leakage in NIBP, or the manual leakage test result

does not exceed 6mmHg/min.

Temp test

The display value of each temperature channel of the monitor does

# Página 45

**Equipo:** Monitor multiparametrico ePM

4-22

not exceed 37 ± 0.1°C

IBP test

Static pressure display value of each IBP channel does not exceed

200 ± 2mmHg

The ART and LV waveforms of each IBP channel are displayed

correctly

C.O. test

Monitor’s TB display value does not exceed 37 ± 0.1°C

The displayed C.O. measurement result is 5 ± 0.25L/min.

Mainstream CO 2  test

The mainstream CO 2  zero calibration is successful, and the baseline

of the CO 2  waveform returns to the zero position on the screen.

The CO 2  Apnea alarm is normal.

The CO 2  display value should be 45 ± 2mmHg

Sidestream CO 2  test

After blocking the air inlet of the water tank, the flow rate of the

sidestream CO 2  is <10ml/min, and it alarms CO 2  airway is blocked,

and there is no air leakage

CO 2  display value should be 6 ± 0.2%

Microstream CO 2  test

After the microstream CO 2  is blocked for about 30s, it alarms

CO 2 sampling airway is blocked, and the module has no air leakage

The CO 2  display value should be 45 ± 2mmHg

Nurse call test

Nurse call cable conducts when the monitor alarms

Analog output test

The waveform displayed by the oscilloscope should be consistent

with that displayed on the monitor’s screen.

Electric safety test

Normally the housing leakage current is not more than 100 μA, and

not more than 300 μA in a single fault condition.

Normally the earth leakage current is not more than 300 μA, and not

more than 1000 μA in a single fault condition.

Normally the patient leakage current is not more than 10 μA, and

not more than 50 μA in a single fault condition.

Normally the patient auxiliary current is not more than 10 μA, and

not more than 50 μA in a single fault condition.

Recorder check

Can print ECG waveforms normally with sound consistency and

clarity

Setup should ensure that relevant prompts should be displayed if it

is out of paper or the buckle cambers or other malfunctions, and it

should work normally after recovery

# Página 46

**Equipo:** Monitor multiparametrico ePM

4-23

The alarm recording function of each parameter is normal.

Network printing check

4 The network printer can print an ECG report properly

Battery check

Batteries support monitor to continue to operate normally when AC

power is accidentally disconnected

Battery power supply time meets product’s specifications

Test conclusion:

Pass or not: (Yes   No)

Sign by the tester:                              Test Date:

# Página 47

**Equipo:** Monitor multiparametrico ePM

5-1

5 Troubleshooting

5.1 Introduction

This chapter lists the problems that may occur during the use of the monitor and recommended measures.

Check the monitor as per the table given in this chapter to identify and resolve problems. For more

information on troubleshooting, please contact Mindray after-sales service department.

5.2 Component Replacement

The PCB, main parts and components of the monitor can be replaced. Once PCB failure is identified,

replace the PCB as per the instructions given in the Repair and Disassembly section. Then confirm that the

monitor can work properly and passes all performance tests. For information on replaceable parts, please

refer to  8 Parts .

5.3 Checkup before Starting the Monitor

In addition, it is necessary to check whether the appearance is damaged before starting the machine. In

particular, if the touch screen of the screen assembly is damaged, do not use it.

5.4 Software Version Check

In some troubleshooting, it may involve the compatibility of software version. In this case, you need to

know the monitor configuration and software version. For details about version compatibility, please

contact our after-sales service department. Please follow the steps below to check software version:

Select  [Main Menu] → turn to the third page → select  [Maintenance >>]  from the  [System >>]  column

→ enter the factory maintenance password →  [Version >>] . In the pop-up menu, you can view the

information about the system software version.

5.5 Technical Alarm Messages

This section lists technical alarms, their default priority, indication on alarm reset, and the actions that can

be taken when an alarm occurs.

Technical alarms give different alarm indicators when the alarm system is reset. In this section we classify

the technical alarms into three categories for easy clarification:

 A: technical alarms are cleared. The monitor gives no alarm indications.

# Página 48

**Equipo:** Monitor multiparametrico ePM

5-2

 B: technical alarms are changed to the prompt messages.

 C: the alarm is silenced and a √ appears before the alarm message, indicating that the alarm is

acknowledged.

In the following tables we will use A, B, and C to refer to the indications on alarm reset.

5.5.1 General Technical Alarm Messages

Alarm message Default priority Indication on

alarm reset

Cause and solution

XX Module Error High C XX module does not work properly. Replug

the module, if the alarm persists, contact your

service personnel.

Note: XX represents a measurement or parameter label, such as HR, RR, SpO 2 , EtCO 2 , and so on.

5.5.2 ECG Technical Alarm Messages

Alarm message Default priority Indication on

alarm reset

Cause and solution

ECG Noisy Low/Prompt A The ECG signal is noisy. Check for any possible

sources of signal noise around the cable and

electrode, and check the patient for excessive

motion.

ECG Amplitude Too

Small

Low C The ECG amplitude does not reach the

detected threshold. Check for any possible

source of interference around the cable and

electrode.

ECG Lead Off High, Med, or

Low,

configurable

B The electrode has become detached from the

patient or the lead wire has become

disconnected from the adapter cable. Check

the connections of the electrodes and

leadwires.

ECG XX Lead Off High, Med, or

Low,

configurable

B The electrode has become detached from the

patient or the lead wire has become

disconnected from the adapter cable. Check

the connections of the electrodes and

leadwires.

ECG Signal Invalid Low A Patient skin impedance is too high. Check

ECG electrode application.

ECG Learning Prompt / ECG learning is manually or automatically

triggered.

Cannot Analyze QT Prompt / /

D12L not available Prompt C The current Va and Vb combination does not

support D12L. Choose an available Va and Vb

combination. For more information, see  9.5

Using 6-lead Placement to Derive 12-lead ECG

# Página 49

**Equipo:** Monitor multiparametrico ePM

5-3

Alarm message Default priority Indication on

alarm reset

Cause and solution

(D12L) .

Note: XX represents ECG lead name, for example RL, LL, V, Va, Vb, and so on.

5.5.3 Resp Technical Alarm Messages

Alarm message Default priority Indication on

alarm reset

Cause and solution

Resp Interference Prompt / The respiration circuit is disturbed. Check for

any possible sources of signal noise.

Electrode Poor Contact Prompt / Check the electrode application. Reposition or

replace the electrodes if necessary. 5.5.4 SpO 2  Technical Alarm Messages

Alarm message Default priority Indication on

alarm reset

Cause and solution

SpO2 Sensor Off Adjustable B The SpO 2  sensor has become detached from

the patient or the module. Check the sensor

connection. If the alarm persists, replace the

sensor.

SpO2 No Sensor Low A The SpO 2  extension cable is detached from

the SpO 2  module, or the SpO 2  sensor is

detached from the SpO 2  extension cable.

Check the SpO 2  cable and the sensor

connection. If the alarm

persists, replace the sensor.

SpO2 Excess Light Low C Ambient light is too strong. Move the sensor

to a place with lower level of ambient light or

cover the sensor to minimize the ambient

light.

SpO 2  No Pulse Low C The SpO 2  sensor failed to obtain pulse signal.

Check the patient’s condition and replace the

sensor application site. If the alarm persists,

replace the sensor.

SpO 2  Sensor

Incompatible

Low C Incompatible or an unspecified SpO 2  sensor is

used. Use specified sensors.

SpO 2  Low Signal Quality Low C 1. Check the sensor and sensor position.

2. Make sure the patient is not shivering or

moving.

3. The patient’s pulse may be too low to be

measured.

# Página 50

**Equipo:** Monitor multiparametrico ePM

5-4

Alarm message Default priority Indication on

alarm reset

Cause and solution

SpO 2  Interference Low C The SpO 2  signal has been interfered. Check

for any possible sources of signal noise and

check the patient for excessive motion.

SpO 2  Sensor Error Low C Replace the sensor and measure again.

SpO 2  Searching Pulse Prompt / SpO 2  is searching for pulse.

SpO 2  Low Perfusion Prompt / The SpO 2  sensor is not properly placed or the

patient’s perfusion index is too low.

1. Check the sensor and sensor position.

2. Reposition the sensor if necessary.

5.5.5 Temp Technical Alarm Messages

Alarm message Default priority Indication on

alarm reset

Cause and solution

T XX Sensor Off Low A Check the sensor connection and reconnect

the sensor.

Note: XX represents a temperature site, for example skin, core, axil, T1, and so on.

5.5.6 NIBP Technical Alarm Messages

Alarm message Default priority Indication on

alarm reset

Cause and solution

NIBP Cuff Loose Low A There is a leak in the cuff or air tubing. Use a

cuff of correct type based on the patient size.

Apply the cuff and connect the air tubing as

instructed in the manual.

NIBP Cuff or Airway Leak Low A Check the NIBP cuff and pump for leakages.

NIBP Airway Error Low A The air tubing may be occluded. Check the air

tubing for an occlusion or kinking. If the

alarm persists, contact your service

personnel.

NIBP Weak Signal Low A The patient’s pulse is weak or the cuff is loose.

Check the patient’s condition and replace the

cuff application site.

NIBP Overrange Low A The measured NIBP value exceeds the

module measurement range. Check the

patient’s condition.

NIBP Excessive Motion Low A Check the patient’s condition and reduce

patient motion.

NIBP Cuff Overpressure Low A The NIBP airway may be occluded. Check the

airway and measure again. If the alarm

persists, contact your service personnel.

# Página 51

**Equipo:** Monitor multiparametrico ePM

5-5

NIBP Timeout Low A The measurement time exceeds 120 seconds

in the adult or pediatric mode, or exceeds 90

seconds in the neonatal mode, and the BP

value cannot be obtained. Check the patient’s

condition and NIBP connections, or replace

the cuff and measure again.

NIBP Cuff and Patient

Mismatch

Low A The cuff type mismatches the patient

category. Verify the patient category or

replace the cuff if necessary. If patient

catergory is correct, check that the tubing is

not bent and the airway is not occluded.

NIBP Airway Leak Low A Airway leakage is found during the NIBP

leakage test. Check the NIBP cuff and pump

for leakages.

5.5.7 IBP Technical Alarm Messages

Alarm message Default priority Indication on

alarm reset

Cause and solution

XX Sensor Error Med C The IBP sensor fails. Replace the sensor.

XX No Sensor High, Med, or

Low, configurable

A The IBP patient cable and/or corresponding

IBP sensor is not connected or detached.

Check the cable and sensor connection.

XX No Pulse Low A The catheter may be occluded. Please flush

the catheter.

XX Disconnected High C The liquid way is disconnected from the

patient, or the three-way valve is open to the

air. Check the connection of the liquid way, or

check the valve is open to the patient. If the

alarm persists, contact your service

personnel.

Note: XX represents an IBP label, for example PA, CVP, FAP, P1, and so on.

# Página 52

**Equipo:** Monitor multiparametrico ePM

5-6

5.5.8 C.O. Technical Alarm Messages

Alarm message Default priority Indication on

alarm reset

Cause and solution

TB Sensor Off Low A Check the sensor connection and reconnect

the sensor.

T1 Sensor Off Low A Check the sensor connection and reconnect

the sensor. 5.5.9 CO 2  Technical Alarm Messages

Alarm message Default priority Indication on

alarm reset

Cause and solution

CO 2  Module High Temp Low C Ambient temperature is too high or there is a

module failure.

1. Lower the operating temperature.

2. Replug the module.

3. If the alarm persists, the CO 2  module may

fail, contact your service personnel.

CO 2  Module Low Temp Low C Ambient temperature is too low or there is a

module failure.

1. Raise the operating temperature.

2. Replug the module.

3. If the alarm persists, the CO 2  module may

fail, contact your service personnel.

CO 2  Zero Failed Low C For mainstream CO 2  module, check the

connections between the adapter and CO 2

transducer. Wait till the sensor’s temperature

becomes stabilized, and then perform a zero

calibration again.

For sidestream CO 2  module, replug the

module. If the alarm persists, contact your

service personnel.

CO 2  No Watertrap Low B Check the watertrap connections.

CO 2  High Airway

Pressure

Low C 1. Check the airway pressure settings of the

ventilator/anesthesia machine.

2. Disconnect the module from the

ventilator/ anesthesia machine.

3. Replug the module.

4. If the alarm persists, contact your service

personnel.

# Página 53

**Equipo:** Monitor multiparametrico ePM

5-7

Alarm message Default priority Indication on

alarm reset

Cause and solution

CO 2  Low Airway Pressure Low C 1. Check the airway pressure settings of the

ventilator/anesthesia machine.

2. Disconnect the module from the

ventilator/ anesthesia machine.

3. Replug the module.

4. If the alarm persists, contact your service

personnel.

CO 2  High Barometric Low C The ambient pressure exceeds the operating

pressure range or CO 2  module fails.

1. Make sure that the ambient pressure

meets the specifications, and check for

sources that affect the ambient pressure.

2. Replug the module.

3. If the alarm persists, contact your service

personnel.

CO 2  Low Barometric Low C The ambient pressure exceeds the operating

pressure range or CO 2  module fails.

1. Make sure that the ambient pressure

meets the specifications, and check for

sources that affect the ambient pressure.

2. Replug the module.

3. If the alarm persists, contact your service

personnel.

CO 2  Airway Occluded Low C 1. Check if the sample line is kinked or

occluded.

2. Replace the sample line.

3. Replug the module.

4. If the alarm persists, contact your service

personnel.

CO 2  No Filterline Low A Make sure that the filterline is connected.

CO 2  Calibration Required Low C Perform a calibration.

CO 2  Airway Error Low C 1. Check if the sample line is kinked or

occluded.

2. Replace the sample line.

3. Replug the module.

4. If the alarm persists, contact your service

personnel.

CO 2  Adapter Error Low A Check, clean or replace the airway adapter.

Perform a zero calibration.

CO 2  No Sensor Low A Make sure that the CO 2  transducer is

connected.

# Página 54

**Equipo:** Monitor multiparametrico ePM

5-8

Alarm message Default priority Indication on

alarm reset

Cause and solution

CO 2 : Change Watertrap Low C Replace the watertrap.

CO 2  Watertrap and

Patient Mismatch

Low C Check the patient category and use a correct

watertrap.

CO 2 : Change O 2  Cell Low C The oxygen sesnor is depleted or fails.

Replace the oxygen sensor. 5.5.10 AG Technical Alarm Messages

Alarm message Default priority Indication on

alarm reset

Cause and solution

AG No Watertrap Low B Check the connections of the watertrap and

re- connect it.

AG: Change Watertrap Low C Replace the watertrap.

AG Watertrap and

Patient Mismatch

Low C Check the patient category and use a correct

watertrap.

AG Zero Failed Low C There is external electromagnetic

interference, airway occlusion or module

failure.

1. Check for external inference sources.

2. Check for “AG Airway Occluded” alarm

message. Remove the occlusion.

3. If the alarm persists, contact your service

personnel.

Anesthetic Mixture Low C Anesthetic mixture is detected.

AG Airway Occluded Low C 1. Check if the sample line is occluded.

2. Check the sample line.

3. Replug the module.

4. If the alarm persists, contact your service

personnel. 5.5.11 BIS Technical Alarm Messages

Alarm message Default priority Indication on

alarm reset

Cause and solution

BIS Sensor Off Low A Check and reconnect the BIS sensor. If the

alarm persists, replace the sensor.

BIS Electrode XX Off Low A Check the electrode connection, and

re-attach the electrodes if necessary.

BIS Electrode XX Poor

Contact

Low A Enter the  Sensor Check  menu, and check the

connections of the sensor and electrodes.

BISx Error High C Replug the module. If the alarm persists,

contact your service personnel.

# Página 55

**Equipo:** Monitor multiparametrico ePM

5-9

Alarm message Default priority Indication on

alarm reset

Cause and solution

BIS No Sensor Low A BIS sensor is not properly connected, BIS

cable fails, BISx or BISx4 fails.

1. Check the BIS sensor connection.

2. Replug the BIS module.

3. Replace the BIS cable.

4. Replace BISx or BISx4.

BIS Sensor Too Many

Uses

Low A Replace the sensor.

BIS Sensor Old Low A Replace the sensor.

BIS XX Signal Quality Too

Low

Low A SQI < 15

1. Check the patient’s condition.

2. Check the sensor position, and its contact

with the patient’s skin.

3. Check that BISx or BISx4 is away from the

electrically radiating equipment.

BIS XX Low Signal

Quality

Low A SQI < 15

1. Check the patient’s condition.

2. Check the sensor position, and its contact

with the patient’s skin.

3. Check that BISx or BISx4 is away from the

electrically radiating equipment.

BIS Wrong Sensor Type Low A Check or replace the sensor.

BIS Sensor Error Low C Replace the sensor.

Disconnect/Reconnect

BIS

Low A Replug the BIS Module.

Note: XX represents BIS label, for example G, C, LE, LT, RL-RA, L-R, F-R, 1, 2, and so on.

5.5.12 Power Supply Technical Alarm Messages

Alarm message Default priority Indication on

alarm reset

Cause and solution

Low Battery Med C Connect the monitor to the external power

supply and allow the batteries to charge.

Critically Low Battery High C Connect the monitor to the external power

supply and allow the batteries to charge.

Power Board Comm

Error

High C Restart the monitor. If the alarm persists,

contact your service personnel.

Battery Error High C The battery may fail. Contact your service

personnel.

RT Clock Need Reset High C Contact your service personnel.

RT Clock Not Exist High C Contact your service personnel.

# Página 56

**Equipo:** Monitor multiparametrico ePM

5-10

Alarm message Default priority Indication on

alarm reset

Cause and solution

XX V Too High High C There is a problem with the system power

supply. Restart the monitor. XX V Too Low High C

Note: XX represents 2.5 V, 3.3 V,5 V, or 12 V.

5.5.13 Recorder Technical Alarm Messages

Alarm message Default priority Indication on

alarm reset

Cause and solution

Recorder Init Error Low A An error occurred during the recorder

initialization. If the alarm persists, contact

your service personnel.

Recorder Comm Error Low A Restart the monitor if not solved. If the alarm

persists, contact your service personnel.

Recorder Head Hot Low C The recorder has been working for too long

time. Stop the recording and resume the

recording till the recorder’s print head cools

down.

Recorder Initializing Prompt / Wait until the recorder initialization is

completed.

Recorder out of Paper Prompt / The recorder paper is not loaded or the recorder

door is not closed. Check the recorder, load the

recorder paper or close the recorder door.

Recorder Busy Prompt / The buffer queue for recording is full. 5.5.14 Printer Technical Alarm Messages

Alarm message Default priority Indication on

alarm reset

Cause and solution

Printer Buffer Full Prompt / The printer buffer is full. Wait till the printer

finishes the printing task.

Fail Prompt / The printer runs out of paper or cannot be

connected. Check the printer.

Printing Stopped Prompt / Printing is manually stopped.

Printer Unavailable Prompt / The printer may fail. Check the printer.

PDF storage space is

nearly full

Prompt / Delete the files saved under the PDF file path

to release storage space. Otherwise you

cannot save new PDF files.

Error storing PDF file Prompt / The PDF file path settings on the printer

server and the PDFCreator are not consistent

or the PDF storage space is full. Check the

PDF file path settings for consistency, or

delete the files saved under the PDF file path

to release storage space.

# Página 57

**Equipo:** Monitor multiparametrico ePM

5-11

Alarm message Default priority Indication on

alarm reset

Cause and solution

Change the print server

language to be

consistent with this

monitor

Prompt / Verify that the language settings of the

printer server and the monitor are consistent,

Otherwise you cannot perform printing.

Print Server

Disconnected

Prompt / Check that the monitor is properly connected

with the printer server. 5.5.15 Technical Alarm Messages Related to Networked Monitoring

Alarm message Default

priority

Indication on

alarm reset

Cause and solution

No CMS Low B The monitor is disconnected from the CMS.

Check the network connection.

View Bed XX YY-ZZ,

Network Disconnected.

Low A The network is interrupted when the monitor

is viewing the remote device. Check the

network connection.

Viewed by Bed XX YY-ZZ,

Network Disconnected.

Low A The network is interrupted when the monitor

is viewed by another remote device. Check the

network connection.

WLAN IP Address Conflict Low C Wireless network IP network conflicts. Check

the network settings.

LAN1 IP Address Conflict Low C Wired network LAN1 IP network conflicts.

Check the network settings.

Fail To Get WLAN IP

Address

Low C Unable to automatically obtain the wireless

network IP address. Check the network

settings.

Fail To Get LAN1 IP

Address

Low C Unable to automatically obtain the wired

network LAN1 IP address. Check the network

settings.

Note: XX refers to the department name, YY refers to the room number, and ZZ refers to the bed

number.

5.5.16 Other System Technical Alarm Messages

Alarm message Default priority Indication on

alarm reset

Cause and solution

Storage Card Error High C The storage card fails or files are damaged.

Restart the monitor to format the storage

card. If the alarm persists, contact your service

personnel.

Loading Default Config

Failed

Low A The default configuration is not correctly

loaded. The monitor will restore to the factory

default configuration for the current patient

category.

# Página 58

**Equipo:** Monitor multiparametrico ePM

5-12

Alarm message Default priority Indication on

alarm reset

Cause and solution

XX Conflicts

(XX refers to the module

label)

Prompt / The same type of corresponding module

being used exceeds the supported number.

Remove the conflict module.

XXX Measurement has

been closed

(XX refers to the module

label)

Prompt / The parameter module is disabled. Switch on

the module if you want to use it. For more

information, see  3.11.1 Switching On or Off a

Parameter .

The display setup for

XXX is disabled.

(XX refers to the

parameter label)

Prompt / The parameter of the newly inserted module

is not displayed on the screen. Select a

desired area to display the parameter

numerics and waveforms. For more

information, see  26.11 The Other Settings .

The patient data storage

space is nearly full.

Please delete some

discharged patients.

Configurable B Delete unnecessary earlier discharged

patient.

5.6 Troubleshooting Guide

5.6.1 Problems with Turning on/off

Troubles Possible causes Troubleshooting

Unable to turn

the monitor on

AC power is not connected, or

a low battery or a damaged

battery

 Please confirm if the AC power is connected

properly.

 Check if the battery is low or if the battery is

damaged.

Connection line failure

 Check if the line between the ON/OFF button board

and the main control board is connected properly.

 Check if the plug of the connection line and the

corresponding socket are damaged.

ON/OFF button board is

damaged

Replace the ON/OFF button board

Power module is damaged Replace the power module

The main control board is

damaged

Replace the main control board

Power protection

 If there are other devices connected to the main

unit, such as external parameter modules, USB flash

drives and scanners, disconnect them from the

main unit first. If you can turn it on after the

disconnection, it’s possible that abnormal external

devices trigger power protection.

# Página 59

**Equipo:** Monitor multiparametrico ePM

5-13

Troubles Possible causes Troubleshooting

 If there are no other devices connected to the main

unit, check the backboard of integral module rack

or the main control board to see if there are short

circuits which result in power protection.

Is it able to turn it on?

Yes

No

Please connect AC power, and ensure AC power is outputted properly

Unable to turn it on(powered by battery)

Charge it For 5 min., then disconnect the AC, will the power be off immediately

Yes

Battery malfunction

Yes

Yes

Is the main Control Board connected properly to the front housing button board?

Whether the AC module can output properly?

No

Reconnect the connection line between the main control board and the front housing button board

No

Replace the AC module

Yes

Is the battery displayed to be in place?

Yes

Yes

Inability to turn it on due to low battery

No

Is AC indicator light lit?

No

Is the Power On/Off button board working properly? No

Replace the ON/OFF button board

是

Is the battery backboard properly connected to the main control board No

Reconnect the connection line between the battery backboard and the main control board

Yes

Can the battery backboard work properly?

Yes

No

Replace the battery backboard

Battery malfunction

Check if these modules work abnormally and result in power protection and inability to turn it on

Is the recorder/infrared backboard Of the built-in parameter module (CO/CO2) connected?

Yes

No

The main control board is damaged

Troubleshooting flowchart for the inability to turn it on due to battery failure

# Página 60

**Equipo:** Monitor multiparametrico ePM

5-14

No

Please connect AC power, and ensure AC power is outputted properly

Unable to turn the monitor on

Yes

Yes

Is the main control board connected properly to the front housing button board?

No

Reconnect the connection line between the main control board and the front housing button board

No

Replace the AC module

Yes

Is AC indicator light lit?

Is the Power On/Off button board working properly? No

Replace the ON/OFF button board

Yes

Check if these modules work abnormally and result in power protection and inability to turn it on

Is the recorder/ built-in parameter module(CO/CO2) /infrared backboard connected?

Yes

No

The main control board is damaged

Whether the AC module can output properly?

Is the Power On/Off button board working properly? No

Replace the ON/OFF button board

Yes

Troubleshooting flowchart for the inability to turn it on due to AC power failure

# Página 61

**Equipo:** Monitor multiparametrico ePM

5-15

5.6.2 Display Failures

Troubles Possible causes Troubleshooting

Unable to

display, or

abnormal

display, but the

main unit can

work

Connection line

failure

 Check if the display is properly connected to the main

control board (screen and backlight line).

 Check if the line plug and corresponding socket are

damaged

LCD display is

damaged

Replace the front housing assembly

Main control board

software goes wrong

Update the main control board software

The backlight drive is

damaged

Change the main control board

The display drive is

damaged

Change the main control board

The touch screen

does not

respond.

Connection line

failure

 Check if the touch screen is properly connected to the main

control board

 Check if the line plug and corresponding socket are

damaged

The touch screen is

damaged

Replace the front housing and touch screen repair kit

Main control board

software goes wrong

Update the main control board software

The main control

board is damaged

Change the main control board

# Página 62

**Equipo:** Monitor multiparametrico ePM

5-16

Yes

Can the main control board be started properly?

Yes

No

Are the display signal line and the backlight lines connected properly?

No display on the display screen

Display malfunction/main control board display driver malfunction

Main control board malfunction

No

Reconnect the display signal line and the backlight lines

Display troubleshooting flowchart

5.6.3 Alarm Failures

Troubles Possible causes Troubleshooting

The alarm

indicator light is

always off or

always on, but

the alarm sounds

generated

properly.

Connection line failure

 Check if the alarm light board is properly connected to

the main control board.

 Check if the connection line or plug is damaged.

Alarm indicator light

board is damaged

Replace the alarm indicator light board

The main control board is

damaged

Change the main control board

No alarm sound

is generated, but

the alarm

indicator light

works properly.

Alarm sound is turned off

Check whether the alarm sound is set to be silent; select [Main

Menu] → [System  >> ] → [Maintenance  >> ] → enter the user

maintenance password → [Alarm  >> ], and adjust the

[Minimum Alarm Volume] to an appropriate value in the

pop-up m enu. Select [Alarm] → [Setup] on the main menu to

adjust the alarm volume.

Speaker damage Replace the speaker

Connection line failure

Check if the speaker is properly connected to the main control

board.

The main control board is

damaged

Change the main control board

# Página 63

**Equipo:** Monitor multiparametrico ePM

5-17

5.6.4 Recorder Failures

Troubles Possible causes Troubleshooting

The recorder is

unable to print

Recorder module is not

allowed

Check if the recorder's work indicator light is on.

If it is on, restore its function in the factory maintenance.

There’s a paper jam Reinstall printing paper

Connection line failure

 Check if the recorder is properly connected to the main

control board.

 Check if the connection line or plug is damaged.

The recorder is damaged Replace the recorder

The main control board is

damaged

Change the main control board

Poor printing

effect

Thermal-sensitive

coating of the printing

paper fails

Replace the printing paper

The thermal head is dirty Clean the thermal head

The recorder is damaged Replace the recorder

5.6.5 Output Interface Failures

Troubles Possible causes Troubleshooting

Nurse call signal

is not outputted

The main control board is

damaged

Change the main control board.

USB Device

Unusable.

The main control board is

damaged

Change the main control board.

The network

interface cannot

be used

The main control board is

damaged

Change the main control board.

VGA interface

cannot be used

The display does not

match with the timing

sequence of VGA

interface

Please confirm whether the display supports the resolution of

1280*800 (10-inch/12-inch model) or 1376 * 768 (15-inch).

The main control board is

damaged

Change the main control board.

# Página 64

**Equipo:** Monitor multiparametrico ePM

5-18

5.6.6 Battery Failures

Troubles Possible causes Troubleshooting

Battery cannot

supply power

Battery is damaged Replace the battery

Connection line failure

 Check if the main control board is properly connected

to the battery interface board.

 Check if the connection line or plug is damaged.

The battery

cannot be fully

charged or

cannot be

charged

Battery is damaged Replace the battery

Connection line failure

 Check if the main control board is properly connected

to the battery interface board.

 Check if the connection line or plug is damaged.

The main control board is

damaged

Change the main control board

5.6.7 Parameter Module Failures

Troubles Possible causes Troubleshooting

ECG/Resp/SPO 2  (Mindray)/NIBP/Temp/IBP do

not work

Incorrect software

version

Check the MPM and system

software versions and update the

software

Parameter circuit

is damaged

Change the main control board

Connection line

failure

 Confirm whether the

parameter board and the main

board are properly connected.

 Confirm if these connection

lines and connectors are

intact.

Accessories may

be damaged

Replace the accessories.

Check whether

the parameter

configuration is

correct

According to the user manual,

confirm whether the

corresponding parameter

configuration has been opened

SPO 2  module (nellcor) cannot work

Accessories may

be damaged

Replace accessories

SPO2 module

failure

Replace the module.

CO 2  (built-in) module cannot work

Internal air pipe

connection failure

 Check if the internal air pipe is

properly connected

 Check if the internal air pipe is

damaged

# Página 65

**Equipo:** Monitor multiparametrico ePM

5-19

Troubles Possible causes Troubleshooting

System software

configuration error

Check if the modules in the system

software are configured correctly.

The module is

damaged

Replace the module

Connection line

failure

 Check if the CO 2  module is

properly connected to the

main control board.

 Check if the line is damaged

The main control

board is damaged

Change the main control board

C.O. (built-in) module cannot work

System software

configuration error

Check if the modules in the system

software are configured correctly.

The module is

damaged

Replace the module

Line connection

failure

 Check if the parameter board

is properly connected to the

C.O. module and the C.O.

module is properly connected

to the main control board.

 Check if the connection line is

damaged

The main control

board is damaged

Change the main control board

5.6.8 Network Failures

Troubles Possible causes Troubleshooting

Frequent

disconnection of

network

The network cable is

not properly

connected.

Check if the network cable is connected properly, or whether the

network cable is too close to the power cable of a high-power

device, or whether the network cable is too long (cannot exceed

50m).

Network settings

error

Check for IP conflicts in the network. If yes, reset the network.

The network has

been connected,

the Viewbed

function cannot

be realized

The network cable is

not properly

connected

Check if the network cable is connected properly, or whether the

network cable is too close to the power cable of a high-power

device, or whether the network cable is too long (cannot exceed

50m).

Have got too many

monitors under

observation

Confirm the number of monitors that can be connected at the

same time according to the user manual.

# Página 66

**Equipo:** Monitor multiparametrico ePM

5-20

Troubles Possible causes Troubleshooting

Network settings

error

Check for IP conflicts in the network. If yes, reset the network.

WLAN cannot be

connected

Network settings

error

Check whether WLAN settings are correct.

The antenna is not

properly installed

Please check if the antenna of the wireless network card is

properly connected to the wireless module.

Wireless module is

damaged

Please replace the wireless module.

The main control

board is damaged

Replace the main control board.

5.6.9 Software Upgrade Failures

Troubles Possible causes Troubleshooting

Program

upgrade fails

Connection error

 Check if the network cable is connected to the monitor's

network interface instead of iView's network interface.

 Make sure the hub or switch can work properly and

check if the hub is properly connected.

Program upgrade

package error

Please select the correct upgrade package.

Error in the IP address

setting of PC

Set a fixed IP address for the upgraded monitor within the

specified Class C addresses. It is not recommended to

upgrade the program in a network with multiple PCs

connected.

# Página 67

**Equipo:** Monitor multiparametrico ePM

6-1

6 Upgrade

6.1 Introduction

This monitor supports upgrade of the monitoring parameter function module, function component, and

software.

Precautions

 Before upgrading the function of a monitor to be disassembled, eliminate static electricity.

When disassembling components with electrostatic sensitive mark, wear ESD wristband or

gloves to avoid damage to the components.

 During reinstallation, connect and place cables properly to avoid crushing the cables, which

may cause a short circuit.

 During reinstallation, select screws with proper model. If you forcibly tighten improper screws,

the device may be damaged. And the screws or components may become loose during use,

which causes unpredictable product damage or personal injury.

 Disassemble the device based on the disassembly sequence. Otherwise, an irreversible damage

may be caused to the device.

 Before disassembling components, ensure that all connected cables are removed. During

disassembly, avoid pulling off the cables or damaging the connectors.

 Loosened screws and other parts should be categorized and placed properly so that they can

be used for reinstallation and will not be dropped, polluted or lost.

6.2 Parameter Function Module Upgrade

This monitor supports upgrade of the following parameter function modules:

Embedded Parameter

Module

PN Name and Specification Remarks

IBP module 115-059953-00 Integrated IBP material package FRU

C.O. module 115-059954-00 Integrated C.O. material package FRU

Sidestream CO 2  module

115-059974-00

Integrated 10/12-inch sidestream CO 2

material package FRU

Microstream CO 2  module

115-059956-00

Integrated microstream CO 2  material

package FRU

Mainstream CO 2  module

115-059957-00

Integrated mainstream CO 2  material

package FRU

# Página 68

**Equipo:** Monitor multiparametrico ePM

6-2

For details about the use method of different parameter modules, see ePM series user manual. The

following content describes the upgrade methods of the parameter modules:

6.3 Upgrading Parameter C.O. Function Module

When upgrading the C.O. function, install the upgrade material packag.

The operation procedure is as follows:

1.  Disassemble the main control board by referring to section "Disassembling Main Control Board" in

the Disassembly and Repair part.

2.  Install the C.O. board in the material package to the main control board by referring to

"Disassembling C.O. Board".

```metadata
pagina: 68
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P68_I0.png
contexto: 
```

![Imagen página 68 - 0](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P68_I0.png)

Black insulation sheet C.O. board

Connection cable

Three M3X6 screws

3. Reassemble the machine.

4. Start the monitor, and choose [ Main Menu ] > [ Maintenance ] > [ Factory Maintenance ] > [ Factory

Default ], enable [ C.O. ], and restart the machine to validate the configuration.

5.  Test the upgraded machine by referring to "C.O. Test" in the Module Performance Test part.

6.4 Upgrading the Gas Module

When upgrading the gas function, use the material in the upgrade material package to replace the gas

module, cables connecting the gas module and main control board, and cables connecting the gas

module and parameter face head.

The operation procedure is as follows:

1.  Separate the front and rear housings of the machine by referring to "Disassembling Front and Rear

Housings" in the Disassembly and Repair part.

2.  Connect the mainstream CO 2  module, microstream CO 2  module, and sidestream CO 2  module in the

material package using sheet metals and cables by referring to "Disassembling Gas Module" in the

Disassembly and Repair part. The machine supports only single gas module upgrade.

# Página 69

**Equipo:** Monitor multiparametrico ePM

6-3

```metadata
pagina: 69
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P69_I0.png
contexto: 
```

![Imagen página 69 - 0](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P69_I0.png)

Use three M3X6 screws.

Cable

Mainstream CO 2  module composition diagram

```metadata
pagina: 69
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P69_I1.png
contexto: 
```

![Imagen página 69 - 1](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P69_I1.png)

Cable connecting the microstream CO2 module with the adapter

Cable connecting the mainboard

Three M3X6 screws

Four M3X6 screws

An microstream CO 2  module is used.

```metadata
pagina: 69
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P69_I2.png
contexto: 
```

![Imagen página 69 - 2](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P69_I2.png)

Air filter

Short-circuited hose

Cover

Three M2.5X4 screws

Silicone case

Sidestream CO 2  module composition diagram

3.  Fix the gas module to the bracket of the machine rear housing, and connect it with the main control

board.

# Página 70

**Equipo:** Monitor multiparametrico ePM

6-4

```metadata
pagina: 70
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P70_I0.png
contexto: 
```

![Imagen página 70 - 0](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P70_I0.png)

Gas module socket

4.  Reassemble the machine.

5.  Start the monitor, and choose [ Main Menu ] > [ Maintenance ] > [ Factory Maintenance ] > [ Factory

Default ], select [ Support CO 2  Class ] to correspond with the upgraded gas module, and restart the

machine to validate the configuration.

6.  Test the upgraded machine by referring to "Gas Module Test" in the Module Performance Test part.

6.5 Function Component Upgrade

Precautions

 When upgrading the WiFi and analog output functions of a standard configuration host, use

the board in the material package to replace the board in the monitor, in addition to installing

corresponding function components into the monitor.

This monitor supports upgraded WiFi components and recorder components.

Function

Component

PN Name and Specification Remarks

Recorder 115-059807-00 Recorder material package FRU

WiFi 115-059923-00 Integrated WiFi material package FRU

This monitor is configured with the WiFi function by building a WiFi through a wireless AP. Only the

engineers or personnel specified by Mindray are qualified for the WiFi building and setting as well as

performance test.

6.5.1 Upgrading WiFi Function

When upgrading the WiFi function, use the material in the upgrade material package to replace the WiFi

module and connected dual-band antennas.

The operation procedure is as follows:

# Página 71

**Equipo:** Monitor multiparametrico ePM

6-5

1.  Disassemble the main control board by referring to section "Disassembling Main Control Board" in

the Disassembly and Repair part.

2.  Install the WiFi module to corresponding socket of the main control board by referring to the

"Disassembling WiFi Module", and attach the antennas to corresponding rear housing of the

machine.

```metadata
pagina: 71
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P71_I0.png
contexto: 
```

![Imagen página 71 - 0](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P71_I0.png)

WiFi cable position

Antenna

Tilt and insert the WiFi module and press it to the bottom.

Fix the WiFi module with the WiFi load board using three M2X4 screws.

ePM 10/ePM 10A/ePM 10C Host

```metadata
pagina: 71
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P71_I1.png
contexto: 
```

![Imagen página 71 - 1](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P71_I1.png)

WiFi cable position Antenna

Tilt and insert the WiFi module and press it to the bottom.

Fix the WiFi module with the WiFi load board using three M2X4 screws.

ePM 12/ePM 12A/ePM 12C Machine

```metadata
pagina: 71
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P71_I2.png
contexto: 
```

![Imagen página 71 - 2](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P71_I2.png)

WiFi cable position

Antenna

Tilt and insert the WiFi module and press it to the bottom.

Fix the WiFi module with the WiFi load board using three M2X4 screws.

ePM 15/ePM 15A/ePM 15C Machine

3.  Sort the antennas, install the main control board, and reinstall the machine.

4.  Start the machine, and test whether the WiFi function is normal.

# Página 72

**Equipo:** Monitor multiparametrico ePM

6-6

5.  To use the WiFi function, refer to its user manual.

Precautions

 If the antennas are not installed in the right position, the WiFi signal quality will be affected.

6.5.2 Upgrading Recorder Function

When upgrading the recorder function, use the material in the upgrade material package to replace the

recorder and cables connecting the recorder and main control board.

The operation procedure is as follows:

1.  Separate the front and rear housings of the machine by referring to "Disassembling Front and Rear

Housings" in the Disassembly and Repair part.

2.  Install the recorder to the bracket of the rear housing recorder by referring to "Disassembling

Recorder".

```metadata
pagina: 72
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P72_I0.png
contexto: 
```

![Imagen página 72 - 0](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P72_I0.png)

Fastener

Two M3X6 screws

Insert and connect recorder cable.

Fastener

3.  Fix the recorder module to the bracket of the machine rear housing, and connect it with the main

control board.

```metadata
pagina: 72
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P72_I1.png
contexto: 
```

![Imagen página 72 - 1](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P72_I1.png)

Recorder cable and socket

4.  Reassemble the machine.

5.  Start the monitor, choose [ Main Menu [ > [ Maintenance ] > [ Factory Maintenance ] > [ Factory

Default ], enable [ Recorder ], and restart the machine to validate the configuration.

6.  Start the machine, and test whether the recorder function is normal.

# Página 73

**Equipo:** Monitor multiparametrico ePM

6-7

6.6 Software upgrade

This monitor supports upgrade through a PC, network or USB disk. Using one of the methods, you can

complete update of the monitor machine and peripheral related firmware.

 This monitor can be upgraded using the network upgrade software (PN: 110-006403-00 PC upgrade

tool) of Mindray monitor. The software can directly run on a mobile or desktop PC. You can upgrade

the following programs of the monitor by network connection or using crossover cables to connect

the monitor with a PC.

 The monitor can also be upgraded using USB disk with specified authorization (containing the USB

disk upgrade Bootstrap PN: 110-004854-00). You can upgrade the following programs of the monitor.

Software PN Name and Specification Remarks

System software

package

/ ePM system package /

Module rack

software

/ FPGA chip-write software /

ePM -

multi-parameter

module

/

M51C_Mindray monitoring algorithm

(extensible ARR)

ECG

configuration

software

/

M51C_Mindray monitoring algorithm

(extensible ARR_12-lead ST)

ECG

configuration

software

/

M51C_Mindray monitoring algorithm

(extensible ARR + 12-lead ST +

Glasgow12-lead resting)

ECG

configuration

software

/

M51C_Mindray monitoring algorithm

(extensible ARR + 12-lead ST +

Glasgow12-lead resting)

ECG

configuration

software

/

M51C_Mindray monitoring algorithm (heart

rate meter + Glasgow12-lead diagnosis)

ECG

configuration

software

/

M51C_Mindray monitoring algorithm (heart

rate meter)

ECG

configuration

software

/

M51C_Mindray monitoring algorithm

(extensible ARR + 12-lead ST +

Mindray12-lead resting)

ECG

configuration

software

/

M51C_Mindray monitoring algorithm (fatal

ARR)

ECG

configuration

software

/

DSP (BF70x) Bootstrap of ePM

multi-parameter module

DSP Bootstrap

/

IBP function program of ePM

multi-parameter module

IBP function

upgrade

# Página 74

**Equipo:** Monitor multiparametrico ePM

6-8

Software PN Name and Specification Remarks

program

/

Mindray SpO 2  function program of ePM

multi-parameter module

Mindray SpO 2

function

upgrade

program

/ DSP (BF70x) function program of ePM

multi-parameter module

DSP function

upgrade

program

IBP module / Chip-write software of M03B module /

C.O. module / Chip-write software of M03B module /

M02D module / Program software of M02D function

Power firmware / Chip-write software of power firmware /

Receiver box module / Firmware software of receiver box module /

6.6.1 Network Upgrade Tool 6.6.1.1 Installing Tool Software

1. Click the execution program SystemUpdateTool.exe of the tool software. A page is displayed. Click

to enter the page requiring you to input the  Serial Number .

```metadata
pagina: 74
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P74_I1.png
contexto: 
```

![Imagen página 74 - 1](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P74_I1.png)

2. Input the  Serial Number , and click

to enter the installation position page of the

program. Select corresponding installation folder, and follow the wizard to click

to

complete the installation.

# Página 75

**Equipo:** Monitor multiparametrico ePM

6-9

Appendix: Multilingual Reference Table

Language (English) Language (Chinese) Remarks

ENGLISH 英语 /

SIM.CHINESE 简体中文 /

FRENCH 法语 /

GERMAN 德语 /

ITALIAN 意大利语 /

POLISH 波兰语 /

SPANISH 西班牙语 /

PORTUGUESE 葡萄牙语 /

RUSSIAN 俄语 /

CZECH 捷克语 /

TURKISH 土耳其语 /

HUNGARIAN 匈牙利语 /

Danish 丹麦语 /

Dutch 荷兰语 /

Finnish 芬兰语 /

Norwegian 挪威语 /

Swedish 瑞典语 /

Romanian 罗马尼亚 /

Serbian 塞尔维亚 /

GREEK 希腊语 /

TRA.CHINESE 繁体中文 /

Japanese 日语 /

6.6.1.2 Connecting the Monitor with a PC

Ensure that at least one NIC is installed on a PC correctly. The monitor is connected with the PC through

this NIC.

1. Connect the monitor with the PC using a hub.

 Connect the PC with the hub using a network cable. Insert one end of the network cable to the

NIC slot of the PC, and insert the other end of the network cable to the slot of the hub.

 Connect the monitor with the hub using a network cable. Refer to the PC and hub connection

method. The hub has multiple slots, so it can be connected with at least 5 monitors to upgrade

them concurrently.

2. Modify the IP address of the PC NIC.

# Página 76

**Equipo:** Monitor multiparametrico ePM

6-10

Precautions

 Before running the upgrade program, set the IP address to 77.77.1.xx to ensure normal

upgrade. The gateway and DNS can be set as necessary. For example, the IP address is set to

77.77.1.13, and the subnet mask is set to 255.255.255.0.

Methods of entering the upgrade mode:

 Connect the monitor with a USB keyboard, and press F4+F5 or * repeatedly during startup to enter

the upgrade mode.

 Slide on the touch screen using two or more fingers to enter the upgrade mode during startup.

6.6.1.3 Setting Software Upgrade

Based on the previous configuration requirements, the software upgrade packages of different products

need to be set. The setting is performed and managed by the administrator only. Set system software

upgrade:

1. Download the ePM system software package (stored in the model package directory), run the

installed system (network) upgrade tool software, select [ Select a New Model Package ] >[ Precise.

Tool ], and click [ Open ] and [ Confirm ], as shown in the following figure:

```metadata
pagina: 76
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P76_I0.png
contexto: 
```

![Imagen página 76 - 0](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P76_I0.png)

3

# Página 77

**Equipo:** Monitor multiparametrico ePM

6-11

```metadata
pagina: 77
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P77_I0.png
contexto: 
```

![Imagen página 77 - 0](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P77_I0.png)

2. In the [ Product Type Selection ] dialog box, select [ Precise ] in the [ Select Product Type ].

```metadata
pagina: 77
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P77_I1.png
contexto: 
```

![Imagen página 77 - 1](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P77_I1.png)

The following page is displayed on the PC:

```metadata
pagina: 77
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P77_I2.png
contexto: 
```

![Imagen página 77 - 2](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P77_I2.png)

2

# Página 78

**Equipo:** Monitor multiparametrico ePM

6-12

6.6.2 Software Upgrade 6.6.2.1 Upgrading System Software and Internal Plugin Cable

1. Enter the system upgrade and download page, and click

```metadata
pagina: 78
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P78_I0.png
contexto: 
```

![Imagen página 78 - 0](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P78_I0.png)

.

2. Browse the prepared system software upgrade package files, and verify whether the download

content, including item, checksum, version, and note is correct, and click [ Confirm ].

The [ Start ] hot key is lit up in the main menu.

```metadata
pagina: 78
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P78_I1.png
contexto: 
```

![Imagen página 78 - 1](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P78_I1.png)

3. Confirm that the network cable is connected correctly and the monitor is stopped, and click the

[ Start ] hot key to download the software.

6.6.2.2 Upgrading Module Software

Upgrade the module program files by referring to the System Software Upgrade Method. After they are

upgraded, click [ Stop ] in the upgrade menu, remove the network cable, and stop and restart the monitor.

For details about the network program upgrade method, refer to the user manual and help of the Mindray

monitor network upgrade software or consult the after-sales service personnel of Mindray.

# Página 79

**Equipo:** Monitor multiparametrico ePM

6-13

6.6.3 Upgrade by USB Disk 6.6.3.1 Preparing USB Disk Upgrade Directory Structure

Prepare the following required tool:

 USB disk: 2 GB or larger ordinary FAT USB disk, for example, Kingston or Netac.

1. Create UPGRADE_AMP\Precise in the root directory of the USB disk.

2. Copy the upgrade Bootstrap Precise-Installer.pkg to the UPGRADE_AMP\Precise directory.

3. Copy the upgrade file (PKG or MPKG) to the UPGRADE_AMP\Precise directory.

6.6.3.2 Inserting the USB Disk into the USB Port of the Monitor

Insert the prepared USB disk into any USB port of the main control board.

6.6.3.3 Triggering Upgrade Mode

 Method 1. Slide on the touch screen using two or more fingers to enter the upgrade mode during

startup.

 Method 2: Connect the monitor with a USB keyboard, and press F2+F3, F4+F5, or * repeatedly during

startup to enter the upgrade mode.

6.6.3.4 Selecting Upgrade File

```metadata
pagina: 79
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P79_I0.png
contexto: 
```

![Imagen página 79 - 0](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P79_I0.png)

# Página 80

**Equipo:** Monitor multiparametrico ePM

6-14

 If there is only one upgrade file, it is selected by default. If there are multiple upgrade files, they are

displayed in two columns. A maximum of 16 upgrade files can be displayed, which should not be

exceeded. Click the up/down/right/left keys to switch to required upgrade file.

 Click

```metadata
pagina: 80
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P80_I0.png
contexto: 
```

![Imagen página 80 - 0](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P80_I0.png)

on the touch screen to select an upgrade file downward, or press    on the

keyboard to select one.

 Click

```metadata
pagina: 80
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P80_I1.png
contexto: 
```

![Imagen página 80 - 1](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P80_I1.png)

on the touch screen to select an upgrade file upward, or press    on the

keyboard to select one.

 Click

```metadata
pagina: 80
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P80_I2.png
contexto: 
```

![Imagen página 80 - 2](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P80_I2.png)

on the touch screen to select an upgrade file rightward, or press    on the

keyboard to select one.

 Click

```metadata
pagina: 80
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P80_I3.png
contexto: 
```

![Imagen página 80 - 3](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P80_I3.png)

on the touch screen to select an upgrade file rightward, or press    on the

keyboard to select one.

 Click

```metadata
pagina: 80
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P80_I4.png
contexto: 
```

![Imagen página 80 - 4](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P80_I4.png)

on the touch screen to confirm the selected upgrade file, or press [Enter] on the

keyboard to confirm the selection.

6.6.3.5 Completing Upgrade Process

If the following page is displayed, the upgrade is complete. Stop and restart the monitor to validate the upgrade.

```metadata
pagina: 80
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P80_I5.png
contexto: 
```

![Imagen página 80 - 5](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P80_I5.png)

```metadata
pagina: 80
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P80_I6.png
contexto: 
```

![Imagen página 80 - 6](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P80_I6.png)

# Página 81

**Equipo:** Monitor multiparametrico ePM

6-15

Attention

 Before the upgrade, disconnect the monitor from a patient and save important data in the monitor.

 During upgrade of the Bootstrap and FPGA, do not stop or power off the monitor. Otherwise,

the device will be corrupted.

 Program upgrade can be performed by professional maintenance personnel only. Failure to

avoid any maintenance warning may cause slight personal injury, product fault, or property loss.

Precautions

 After the Bootstrap is upgraded, re-upgrade the system program or other programs to ensure

their compatibility.

 Before upgrade, ensure that the version of the upgrade package is the required one. To obtain

the latest upgrade package, contact the product after-sales service department of this company.

# Página 82

**Equipo:** Monitor multiparametrico ePM

7-1

7 Maintenance and Disassembly

7.1 Tool

Before disassembling or replacing parts, the following tools may be used:

 Small Phillips screwdriver

 Phillips screwdriver

 Tweezers

 Needle-nose pliers

 Cutting pliers

7.2 Preparations

Before disassembling the monitor, make the following preparations:

 Stop monitoring the patient, power off the monitor, and disconnect all attachments and external

devices.

Warnings

 Before disassembly, eliminate static electricity. When disassembling components with

electrostatic sensitive mark, wear ESD wristband or gloves to avoid damage to the

components.

 During reinstallation, connect and place cables properly to avoid crushing the cables, which

may cause a short circuit.

 During reinstallation, select screws with proper model. If you forcibly tighten improper screws,

the device may be damaged. And the screws or components may become loose during use,

which causes unpredictable product damage or personal injury.

 Disassemble the device based on the disassembly sequence. Otherwise, an irreversible damage

may be caused to the device.

 Loosened parts should be categorized and placed properly so that they can be used for

reinstallation and will not be dropped, polluted or lost.

 During reinstallation, install the components prior to the host, and connect and place cables

and hoses properly.

 The machine has waterproof requirement. During reinstallation, ensure that waterproof case

and other waterproof materials are assembled properly.

# Página 83

**Equipo:** Monitor multiparametrico ePM

7-2

7.3 ePM 15/ePM 15A/ePM 15C Host Disassembly

7.3.1 Disassembling Front/rear Housing Components of Host

1. Use a Phillips screwdriver to loosen four M4X8 screws.

2. Open the front/rear housings, and remove the display screen connection cable and keypad

connection cable.

Note: During reassembly, close the front/rear covers and pull the cables upward using a hand.

```metadata
pagina: 83
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P83_I0.png
contexto: 
```

![Imagen página 83 - 0](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P83_I0.png)

```metadata
pagina: 83
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P83_I1.png
contexto: 
```

![Imagen página 83 - 1](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P83_I1.png)

Four M4X8 screws

```metadata
pagina: 83
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P83_I2.png
contexto: 
```

![Imagen página 83 - 2](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P83_I2.png)

```metadata
pagina: 83
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P83_I3.png
contexto: 
```

![Imagen página 83 - 3](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P83_I3.png)

```metadata
pagina: 83
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P83_I4.png
contexto: 
```

![Imagen página 83 - 4](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P83_I4.png)

Before closing the front/rear covers, pull the cables upward using a hand.

# Página 84

**Equipo:** Monitor multiparametrico ePM

7-3

7.3.2 Disassembling Keypad and Switch Board

1. Remove the keypad connection cable, loosen the three ST3.3X8 screws shown in the figure, and take

the keypad out.

2. Remove the switch board connection cable, loosen the two ST3.3X8 screws shown in the figure, and

take the switch board out.

7.3.3 Disassembling Display Screen and Alarm Indicator

1. Remove the five cable ties from cables.

2. Remove the cables connecting with the touch screen, display screen, and alarm indicator.

3. Loosen the sticker connecting the touch screen PFC with the sheet metal and the cable stuck to the

sheet metal.

```metadata
pagina: 84
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P84_I0.png
contexto: 
```

![Imagen página 84 - 0](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P84_I0.png)

Three ST3.3X8 screws

Keypad connection cable

Three ST3.3X8 screws

Switch board connection cable

```metadata
pagina: 84
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P84_I1.png
contexto: 
```

![Imagen página 84 - 1](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P84_I1.png)

Loosen the cable sticker.

Five cable ties

# Página 85

**Equipo:** Monitor multiparametrico ePM

7-4

4. Loosen the ten ST3.3X8 screws shown in the figure, and remove the display screen component.

5. Loosen the two M3X6 screws, and take the alarm indicator board out.

6. Loosen the two M3X6 screws with the mark "b" on the right top of the sheet metal.

7. Loosen the two M2X4 screws at the left side of the sheet metal.

8. Loosen the two M2X4 screws at the left side of the sheet metal, and take the display screen out.

```metadata
pagina: 85
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P85_I0.png
contexto: 
```

![Imagen página 85 - 0](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P85_I0.png)

Loosen the cable connection. Loosen the cable sticker.

Loosen the FPC sticker.

```metadata
pagina: 85
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P85_I1.png
contexto: 
```

![Imagen página 85 - 1](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P85_I1.png)

Ten ST3.3X8 screws with the sheet metal mark "a"

```metadata
pagina: 85
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P85_I2.png
contexto: 
```

![Imagen página 85 - 2](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P85_I2.png)

# Página 86

**Equipo:** Monitor multiparametrico ePM

7-5

9. Loosen the sticker connecting the touch screen with the front housing, and tilt and take the touch

screen out.

Note 1. During reassembly of the touch screen rubber, follow the requirements below to perform

assembly.

```metadata
pagina: 86
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P86_I0.png
contexto: 
```

![Imagen página 86 - 0](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P86_I0.png)

```metadata
pagina: 86
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P86_I1.png
contexto: 
```

![Imagen página 86 - 1](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P86_I1.png)

```metadata
pagina: 86
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P86_I2.png
contexto: 
```

![Imagen página 86 - 2](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P86_I2.png)

Two M3X6 screws Two M3X6 screws

Two M3X6 screws

```metadata
pagina: 86
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P86_I3.png
contexto: 
```

![Imagen página 86 - 3](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P86_I3.png)

```metadata
pagina: 86
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P86_I4.png
contexto: 
```

![Imagen página 86 - 4](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P86_I4.png)

When taking the touch screen out, hold the bottom with a hand to support the touch screen up.

Hold the touch screen glass with hand, and do not take the FPC soft chip.

Wash off the double-sided tape.

# Página 87

**Equipo:** Monitor multiparametrico ePM

7-6

Note 2. During reassembly of the touch screen, follow the requirements below to perform assembly.

Note 3. After reassembly of the touch screen, follow the requirements below to press the touch screen.

```metadata
pagina: 87
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P87_I0.png
contexto: 
```

![Imagen página 87 - 0](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P87_I0.png)

```metadata
pagina: 87
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P87_I1.png
contexto: 
```

![Imagen página 87 - 1](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P87_I1.png)

```metadata
pagina: 87
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P87_I2.png
contexto: 
```

![Imagen página 87 - 2](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P87_I2.png)

Amplified

The middle framed hole in the front housing is the display area of the display screen, and so double-sided tape cannot be stuck to this display area.

1. Stick the double-sided tape in alignment with the mark line at the bottom.

2. Stick the double-sided tape in alignment with the mark lines at both outer laterals.

Amplified

Note: The product is configured with a light sensor, so a small hole will be found in this position of the front housing.

Note  ④ . The pit of the top double-sided tape is upward.

Note  ① . The pit of the bottom double-sided tape is upward.  ②  The protrusion of the lateral double-sided tape needs to be put in this pit.

Note  ③ . When sticking the short double-sided tape at the bottom, use the pit position of the long double-sided tape at the bottom as the baseline.

3. Stick the double-sided tape in alignment with the mark line on the top.

```metadata
pagina: 87
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P87_I3.png
contexto: 
```

![Imagen página 87 - 3](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P87_I3.png)

Tilt the touch screen, and put it in from the protrusion of the front housing.

When putting the touch screen in, hold the bottom with a hand to support the touch screen up and avoid the touch screen from touching the double-sided tape.

Hold the touch screen glass with hand, and do not take the FPC soft chip.

# Página 88

**Equipo:** Monitor multiparametrico ePM

7-7

7.3.4 Disassembling WiFi and Parameter Panel

1. Remove cables.

Note. During reassembly, follow the requirements below to perform binding and fixing.

```metadata
pagina: 88
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P88_I0.png
contexto: 
```

![Imagen página 88 - 0](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P88_I0.png)

Press the orange area of the touch screen.

```metadata
pagina: 88
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P88_I1.png
contexto: 
```

![Imagen página 88 - 1](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P88_I1.png)

```metadata
pagina: 88
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P88_I2.png
contexto: 
```

![Imagen página 88 - 2](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P88_I2.png)

Cut binding straps.

Recorder cable (optional)

Rear alarm indicator cable (optional)

Speaker cable

CO2 gas module cable (optional)

```metadata
pagina: 88
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P88_I3.png
contexto: 
```

![Imagen página 88 - 3](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P88_I3.png)

Penetrate the binding strap through the hole.

Bind the cables of the speaker, WiFi, recorder, rear alarm indicator and gas module (optional) using the cables ties.

Insert the rear alarm indicator cable into the slot.

# Página 89

**Equipo:** Monitor multiparametrico ePM

7-8

2. When WiFi is configured, disassemble the WiFi module.

A. Take the WiFi module out.

B. Remove the WiFi cable.

C. Loosen the three M2X4 screws fixing the WiFi module and WiFi load board, and take the WiFi module

and WiFi load board out.

Note. During reassembly of the WiFi module, follow the requirements below to perform assembly.

3. When mainstream CO 2  is configured, disassemble the CO 2  module.

Remove the cables pointed by the arrows in the following figure, loosen three ST3.3X8 cross pan head

tapping screws using the screwdriver, and take the module out.

```metadata
pagina: 89
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P89_I0.png
contexto: 
```

![Imagen página 89 - 0](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P89_I0.png)

Tilt and insert the WiFi module and press it to the bottom.

WiFi cable (optional)

```metadata
pagina: 89
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P89_I1.png
contexto: 
```

![Imagen página 89 - 1](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P89_I1.png)

Fix the WiFi module with the WiFi load board using three M2X4 screws.

Antenna

```metadata
pagina: 89
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P89_I2.png
contexto: 
```

![Imagen página 89 - 2](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P89_I2.png)

```metadata
pagina: 89
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P89_I3.png
contexto: 
```

![Imagen página 89 - 3](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P89_I3.png)

Tilt and insert the WiFi module and press it to the bottom.

Amplified

Stick the antenna to the lateral in alignment with the lower edge of this area.

# Página 90

**Equipo:** Monitor multiparametrico ePM

7-9

4. When microstream CO 2  is configured, disassemble the CO 2  module.

A. Loosen three ST3.3X8 cross pan head tapping screws using the screwdriver, and take the module out.

B. Remove the connection between the microstream module exhaust hose and panel exhaust hose.

Note. During reassembly of the microstream CO 2  module, follow the requirements below to perform

assembly.

5. When sidestream CO 2  is configured, disassemble the CO 2  module.

```metadata
pagina: 90
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P90_I0.png
contexto: 
```

![Imagen página 90 - 0](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P90_I0.png)

Three ST3.3X8 screws

Cable

```metadata
pagina: 90
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P90_I1.png
contexto: 
```

![Imagen página 90 - 1](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P90_I1.png)

```metadata
pagina: 90
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P90_I2.png
contexto: 
```

![Imagen página 90 - 2](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P90_I2.png)

Three ST3.3X8 screws Exhaust hose

```metadata
pagina: 90
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P90_I3.png
contexto: 
```

![Imagen página 90 - 3](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P90_I3.png)

Three ST3.3X8 screws

The panel cables are wound two circles in this position.

The cables here are set aside to avoid being crushed.

Lead the two exhaust hoses connected with the panel through the module bottom.

# Página 91

**Equipo:** Monitor multiparametrico ePM

7-10

A. Loosen the cable ties shown in the following figure, take the three ST3.3X8 cross pan head tapping

screws out, and take the sidestream CO 2  module out.

B. Take the exhaust hose connected with the sidestream CO 2  module out.

B. Loosen the cable connection, and take the module out.

```metadata
pagina: 91
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P91_I0.png
contexto: 
```

![Imagen página 91 - 0](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P91_I0.png)

The cables and exhaust hoses are bound with binding straps.

```metadata
pagina: 91
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P91_I1.png
contexto: 
```

![Imagen página 91 - 1](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P91_I1.png)

Three ST3.3X8 screws

```metadata
pagina: 91
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P91_I2.png
contexto: 
```

![Imagen página 91 - 2](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P91_I2.png)

The transparent exhaust hose connected with the water tank is connected with the nozzle at the left lower side.

Connect the panel exhaust hose.

```metadata
pagina: 91
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P91_I3.png
contexto: 
```

![Imagen página 91 - 3](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P91_I3.png)

Insert cables.

# Página 92

**Equipo:** Monitor multiparametrico ePM

7-11

C. Disassemble the two PT2.0X6 screws on the panel water tank, and take the water tank out.

Note. During reassembly of the sidestream CO 2  module, follow the requirements below to perform

assembly.

6. Remove the panel cable from the mainboard, and remove the NIBP exhaust hose.

7. Loosen two ST3.3X8 cross pan head tapping screws using the screwdriver, and take the panel fixing

pin and panel component out.

```metadata
pagina: 92
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P92_I0.png
contexto: 
```

![Imagen página 92 - 0](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P92_I0.png)

Two PT2.0X6 screws

```metadata
pagina: 92
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P92_I1.png
contexto: 
```

![Imagen página 92 - 1](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P92_I1.png)

M02D cable

```metadata
pagina: 92
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P92_I2.png
contexto: 
```

![Imagen página 92 - 2](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P92_I2.png)

Transparent hose Condensate hose

```metadata
pagina: 92
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P92_I3.png
contexto: 
```

![Imagen página 92 - 3](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P92_I3.png)

The transparent exhaust hose connected with the water tank is connected with the nozzle at the left lower side.

Connect the condensate hose to the upper nozzle.

Connect the panel exhaust hose.

The transparent exhaust hose and condensate hose in this position are led through the front side.

```metadata
pagina: 92
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P92_I4.png
contexto: 
```

![Imagen página 92 - 4](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P92_I4.png)

The cables and exhaust hoses are bound with binding straps.

The condensate hose is wound one circle in this position and bound using binding straps.

# Página 93

**Equipo:** Monitor multiparametrico ePM

7-12

8. When a mainstream module is configured, disassemble the mainstream panel port.

A. Use pliers or tweezers to jack the fastener on the panel, and take the interface board out.

B. Rotate the cable anticlockwise, and remove the CO 2  cable.

C. Remove the plug from the panel.

D. Loosen the M5 screw from the upper right corner of the panel, and take the nozzle out.

Note 1. During reassembly, the interface board of the mainstream panel should be in the following

direction.

```metadata
pagina: 93
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P93_I0.png
contexto: 
```

![Imagen página 93 - 0](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P93_I0.png)

```metadata
pagina: 93
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P93_I1.png
contexto: 
```

![Imagen página 93 - 1](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P93_I1.png)

C.O. cable (optional)

IBP cable (optional)

SpO2 cable

Temp cable

ECG cable

NIBP hose

Two ST3.3X8 screws

```metadata
pagina: 93
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P93_I2.png
contexto: 
```

![Imagen página 93 - 2](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P93_I2.png)

```metadata
pagina: 93
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P93_I3.png
contexto: 
```

![Imagen página 93 - 3](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P93_I3.png)

```metadata
pagina: 93
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P93_I4.png
contexto: 
```

![Imagen página 93 - 4](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P93_I4.png)

```metadata
pagina: 93
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P93_I5.png
contexto: 
```

![Imagen página 93 - 5](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P93_I5.png)

Plug Nipple Nut

# Página 94

**Equipo:** Monitor multiparametrico ePM

7-13

Note 2. During reassembly of the cable to the interface board, tighten it firmly anticlockwise.

9. When an microstream module is configured, disassemble the microstream water tank.

A. Use pliers or tweezers to jack the fastener on the panel, and take the microstream water tank base out.

B. Loosen the M5 screw from the upper right corner of the panel, and take the exhaust nozzle out.

C. Use tweezers to loosen the fastener on the water tank base, and take the microstream connector out.

```metadata
pagina: 94
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P94_I0.png
contexto: 
```

![Imagen página 94 - 0](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P94_I0.png)

```metadata
pagina: 94
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P94_I1.png
contexto: 
```

![Imagen página 94 - 1](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P94_I1.png)

Protrusion upward

Amplified

```metadata
pagina: 94
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P94_I2.png
contexto: 
```

![Imagen página 94 - 2](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P94_I2.png)

Rotate the signal cable fastener anticlockwise to stick to this position.

# Página 95

**Equipo:** Monitor multiparametrico ePM

7-14

10. When a sidestream module is configured, disassemble the sidestream water tank.

A. Remove the cable or hose from the water tank.

B. Remove the exhaust hose from the panel, loosen the M4 screw on the exhaust nozzle, and take the

nozzle out.

C. Loosen the M5 screw/M4 nut on the panel, and take the exhaust nozzle out.

D. Loosen the four PT2.0X6 screws on the panel, and take the bracket of the sidestream water tank out.

11. Disassemble the panel cable.

A. According to the figure, rotate different parameter cables anticlockwise, and remove them.

B. Take the arrival reminding shrapnel out.

```metadata
pagina: 95
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P95_I0.png
contexto: 
```

![Imagen página 95 - 0](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P95_I0.png)

Nipple Nut

```metadata
pagina: 95
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P95_I1.png
contexto: 
```

![Imagen página 95 - 1](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P95_I1.png)

Loosen fastener.

```metadata
pagina: 95
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P95_I2.png
contexto: 
```

![Imagen página 95 - 2](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P95_I2.png)

M02D cable

```metadata
pagina: 95
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P95_I3.png
contexto: 
```

![Imagen página 95 - 3](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P95_I3.png)

Transparent hose Condensate hose

```metadata
pagina: 95
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P95_I4.png
contexto: 
```

![Imagen página 95 - 4](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P95_I4.png)

M4 nut and exhaust nozzle

```metadata
pagina: 95
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P95_I5.png
contexto: 
```

![Imagen página 95 - 5](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P95_I5.png)

# Página 96

**Equipo:** Monitor multiparametrico ePM

7-15

Note. During reassembly, follow the requirements below to perform cable assembling.

```metadata
pagina: 96
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P96_I0.png
contexto: 
```

![Imagen página 96 - 0](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P96_I0.png)

Optional: C.O. cable ECG cable

SpO2 cable

Optional: IBP cable 1 channel (black)

Optional: IBP cable 2 channel (gray)

Temp 1 channel (red)

Temp 2 channel (blue)

Diagram (CO2 gas module is not used)

```metadata
pagina: 96
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P96_I1.png
contexto: 
```

![Imagen página 96 - 1](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P96_I1.png)

When the IBP function is selected

C.O. function

Disassemble the arrival reminding shrapnel.

Shrapnel

Shrapnel

```metadata
pagina: 96
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P96_I2.png
contexto: 
```

![Imagen página 96 - 2](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P96_I2.png)

Optional: IBP cable 1 channel (black)

Optional: IBP cable 2 channel (gray)

Temp 1 channel (red)

Temp 2 channel (blue)

Diagram (CO2 gas module is used)

Optional: C.O. cable

SpO2 cable ECG cable

```metadata
pagina: 96
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P96_I3.png
contexto: 
```

![Imagen página 96 - 3](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P96_I3.png)

When the IBP function is selected

Disassemble the arrival reminding shrapnel.

Shrapnel Shrapnel

When the C.O. function is selected

# Página 97

**Equipo:** Monitor multiparametrico ePM

7-16

12. Disassemble the NIBP nozzle: Rotate the NIBP nozzle anticlockwise, and disassemble the NIBP nozzle.

7.3.5 Disassembling Gas Module

1. When mainstream CO 2  is configured:

A. Loosen the three M3X6 screws in the figure, and take the mainstream CO 2  isolation power board out.

B. Remove the cable connecting the mainstream isolation power board with the mainboard.

2. When microstream CO 2  is configured:

A. Remove the cable connecting the microstream CO 2  module with the adapter.

B. Remove the cable connecting the mainboard.

C. Loosen the four M3X6 screws in the figure, and take the microstream CO 2  module out.

D. Loosen the three M3X6 screws, and take the adapter out.

```metadata
pagina: 97
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P97_I0.png
contexto: 
```

![Imagen página 97 - 0](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P97_I0.png)

```metadata
pagina: 97
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P97_I1.png
contexto: 
```

![Imagen página 97 - 1](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P97_I1.png)

Rotate the temp socket anticlockwise and stick it to the locating slot.

Rotate other sockets anticlockwise and stick them to the locating slot.

Cable connector assembly diagram

```metadata
pagina: 97
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P97_I2.png
contexto: 
```

![Imagen página 97 - 2](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P97_I2.png)

```metadata
pagina: 97
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P97_I3.png
contexto: 
```

![Imagen página 97 - 3](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P97_I3.png)

Diagram (CO2 module is not configured)

Diagram (CO2 module is configured)

NIBP nozzle component

```metadata
pagina: 97
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P97_I4.png
contexto: 
```

![Imagen página 97 - 4](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P97_I4.png)

```metadata
pagina: 97
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P97_I5.png
contexto: 
```

![Imagen página 97 - 5](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P97_I5.png)

Use three M3X6 screws.

Cable

# Página 98

**Equipo:** Monitor multiparametrico ePM

7-17

3. When sidestream CO 2  is configured:

A. Loosen the two M3X6 screws in the figure, and take the sidestream gas module out.

B. Take the air filter and short-circuited hose out.

C. Loosen the three M2.5X4 countersunk screws, and take the cover out.

D. Take the silicone case out.

7.3.6 Disassembling Recorder/Recorder Bracket

1. When the recorder is configured, disassemble the recorder:

A. Loosen the two M3X6 screws of the recorder, loosen the two fasteners of the recorder, and take the

recorder out.

B. Remove the cable connecting the two sockets of the recorder.

```metadata
pagina: 98
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P98_I0.png
contexto: 
```

![Imagen página 98 - 0](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P98_I0.png)

```metadata
pagina: 98
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P98_I1.png
contexto: 
```

![Imagen página 98 - 1](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P98_I1.png)

Four M3X6 screws

Cable connecting the mainboard

Cable connecting the microstream CO2 module with the adapter

Three M3X6 screws

```metadata
pagina: 98
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P98_I2.png
contexto: 
```

![Imagen página 98 - 2](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P98_I2.png)

Use two M3X6 screws.

```metadata
pagina: 98
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P98_I3.png
contexto: 
```

![Imagen página 98 - 3](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P98_I3.png)

Air filter

Short-circuited hose

```metadata
pagina: 98
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P98_I4.png
contexto: 
```

![Imagen página 98 - 4](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P98_I4.png)

Three M2.5X4 screws

Cover

```metadata
pagina: 98
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P98_I5.png
contexto: 
```

![Imagen página 98 - 5](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P98_I5.png)

Take the silicone case out.

# Página 99

**Equipo:** Monitor multiparametrico ePM

7-18

2. Take the recorder bracket out: Loosen the two ST3.3X8 screws on the recorder bracket, and take the

recorder bracket out.

7.3.7 Disassembling Main Bracket Component

1. Loosen the battery cover.

2. Loosen the five ST3.3X8 screws shown in the figure, and remove the main bracket component.

```metadata
pagina: 99
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P99_I0.png
contexto: 
```

![Imagen página 99 - 0](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P99_I0.png)

Two M3X6 screws

Fastener Fastener

```metadata
pagina: 99
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P99_I1.png
contexto: 
```

![Imagen página 99 - 1](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P99_I1.png)

Insert and connect recorder cable.

```metadata
pagina: 99
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P99_I2.png
contexto: 
```

![Imagen página 99 - 2](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P99_I2.png)

Two ST3.3X8 screws

Recorder bracket

```metadata
pagina: 99
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P99_I3.png
contexto: 
```

![Imagen página 99 - 3](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P99_I3.png)

Open the battery cover.

```metadata
pagina: 99
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P99_I4.png
contexto: 
```

![Imagen página 99 - 4](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P99_I4.png)

Use six ST3.3X8 screws.

# Página 100

**Equipo:** Monitor multiparametrico ePM

7-19

Note 1. Before reassembling the main bracket component, insert the connection belt of the battery cover

to the locating post of the rear housing shown in the following figure.

Note 2. Before closing the battery cover, switch the battery to the vertical position shown in the figure.

7.3.8 Disassembling Speaker

1. Loosen the two ST3.3X8 screws of the speaker component shown in the figure, and take the speaker

component out.

Note. During reassembly of the speaker, follow the requirements below to perform assembly.

```metadata
pagina: 100
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P100_I0.png
contexto: 
```

![Imagen página 100 - 0](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P100_I0.png)

```metadata
pagina: 100
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P100_I1.png
contexto: 
```

![Imagen página 100 - 1](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P100_I1.png)

Put the battery cover aside, without closing it.

Amplified

```metadata
pagina: 100
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P100_I2.png
contexto: 
```

![Imagen página 100 - 2](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P100_I2.png)

After the battery is switched to the vertical position, close the battery cover.

```metadata
pagina: 100
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P100_I3.png
contexto: 
```

![Imagen página 100 - 3](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P100_I3.png)

Two ST3.3X8 screws

```metadata
pagina: 100
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P100_I4.png
contexto: 
```

![Imagen página 100 - 4](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P100_I4.png)

Insert the connection belt of the battery cover to the locating post of the rear housing.

# Página 101

**Equipo:** Monitor multiparametrico ePM

7-20

7.3.9 Disassembling Rear Alarm Indicator (Configured)

1. Loosen the eight ST3.3X8 screws on the cover component shown in the figure, and take the top cover

component out.

2. Loosen the one ST3.3X8 screw on the rear alarm indicator shown in the figure, and take the rear alarm

indicator component out.

7.3.10 Disassembling Power Module

1. Remove the AC input cable, and remove the cable connecting the power module with mainboard

out.

2. Loosen the four M3X6 screws of the power module, and take the power module out.

```metadata
pagina: 101
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P101_I0.png
contexto: 
```

![Imagen página 101 - 0](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P101_I0.png)

Speaker outbound cable

Use two ST3.3X8 screws to fix the speaker.

Insert the cable to the slot.

```metadata
pagina: 101
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P101_I1.png
contexto: 
```

![Imagen página 101 - 1](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P101_I1.png)

```metadata
pagina: 101
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P101_I2.png
contexto: 
```

![Imagen página 101 - 2](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P101_I2.png)

AC input cable

Cable connecting the mainboards

Four M3X6 screws

# Página 102

**Equipo:** Monitor multiparametrico ePM

7-21

7.3.11 Disassembling SpO 2  Module (When Nellcor/Massimo SpO 2  Is Configured)

1. When Nellcor SpO 2  is configured:

Loosen the one M2X4 screw on the Nellcor SpO 2 , and take the Nellcor SpO 2  board out.

2. When Massimo SpO 2  is configured:

Loosen the two M2X4 screws on the Massimo SpO 2 , and take the Massimo SpO 2  board and insulation

sheet out.

7.3.12 Disassembling C.O. Board (Configured)

1. Remove the cable connecting the C.O. board with the mainboard.

2. Loosen the two M3X6 screws on the Massimo SpO 2 , and take the C.O. board and insulation sheet out.

```metadata
pagina: 102
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P102_I0.png
contexto: 
```

![Imagen página 102 - 0](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P102_I0.png)

One M2X4 screw

Assemble Nellcor SpO2 board.

```metadata
pagina: 102
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P102_I1.png
contexto: 
```

![Imagen página 102 - 1](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P102_I1.png)

```metadata
pagina: 102
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P102_I2.png
contexto: 
```

![Imagen página 102 - 2](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P102_I2.png)

Assemble Massimo SpO 2  board.

Use two M3X6 screws.

SpO 2  board insulation sheet

# Página 103

**Equipo:** Monitor multiparametrico ePM

7-22

7.3.13 Disassembling Mainboard

1. Remove the pump/valve connection cables from the mainboard.

2. Take the two interfaces of the NIBP hose from the mainboard sensor.

3. Remove the connection cable of the battery adapter from the mainboard.

4. When two batteries are configured, remove the connection cable of the 2# battery adapter from the

mainboard in the figure.

```metadata
pagina: 103
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P103_I0.png
contexto: 
```

![Imagen página 103 - 0](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P103_I0.png)

C.O. board Black insulation sheet

Three M3X6 screws

Connection cable

```metadata
pagina: 103
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P103_I1.png
contexto: 
```

![Imagen página 103 - 1](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P103_I1.png)

Gas pump connection cable Gas valve connection cable

Two interfaces connecting the NIBP hose and mainboard sensor

```metadata
pagina: 103
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P103_I2.png
contexto: 
```

![Imagen página 103 - 2](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P103_I2.png)

Two connection cables of the 1# battery adapter

# Página 104

**Equipo:** Monitor multiparametrico ePM

7-23

5. Loosen the six M3X6 screws from the main bracket in the figure.

6. Loosen the two screws on the rear of the main bracket sheet metal, and take the mainboard out.

7. As shown in the following figure, loosen the nuts or screws on the rear of the mainboard, and take

the studs out.

```metadata
pagina: 104
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P104_I0.png
contexto: 
```

![Imagen página 104 - 0](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P104_I0.png)

Two connection cables of the 2# battery adapter

```metadata
pagina: 104
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P104_I1.png
contexto: 
```

![Imagen página 104 - 1](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P104_I1.png)

```metadata
pagina: 104
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P104_I2.png
contexto: 
```

![Imagen página 104 - 2](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P104_I2.png)

Two screws

Six M3X6 screws

```metadata
pagina: 104
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P104_I3.png
contexto: 
```

![Imagen página 104 - 3](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P104_I3.png)

```metadata
pagina: 104
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P104_I4.png
contexto: 
```

![Imagen página 104 - 4](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P104_I4.png)

When the C.O. function is selected, there are three M3 nuts here.

When the Masimo SpO2 is selected, there are two M3 nuts here.

When the Nellcor SpO2 is selected, there is one M2 nut here.

When the C.O. function is selected, there are three studs here.

When the Masimo SpO2 is selected, there are two studs here.

When the Nellcor SpO2 is selected, there is one stud here.

# Página 105

**Equipo:** Monitor multiparametrico ePM

7-24

7.3.14 Disassembling Power Adapter and NIBP Pump/Valve

1. As shown in the following figure, loosen the two ST3.3X8 screws, and take the 1# battery adapter out.

2. When 2# battery adapter is configured, loosen the two ST3.3X8 screws, and take the 2# battery

adapter out.

Note. During reassembly of 2# battery adapter, follow the requirements below to perform cable assembly.

3. Loosen the hose connecting the NIBP pump/valve.

4. Loosen the fastener fixing the NIBP valve, and take the NIBP valve out.

5. Loosen the two binding straps fixing the NIBP pump, and take the NIBP pump out.

```metadata
pagina: 105
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P105_I0.png
contexto: 
```

![Imagen página 105 - 0](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P105_I0.png)

1# battery adapter

2# battery adapter

```metadata
pagina: 105
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P105_I1.png
contexto: 
```

![Imagen página 105 - 1](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P105_I1.png)

Lead the cables through the two fasteners.

Penetrate the hole here.

# Página 106

**Equipo:** Monitor multiparametrico ePM

7-25

Note: During reassembly, ensure that the hose is correctly connected with the quick/slow release valve.

```metadata
pagina: 106
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P106_I0.png
contexto: 
```

![Imagen página 106 - 0](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P106_I0.png)

Two binding straps Loosen the fastener fixing the NIBP valve.

Loose the hose connecting the pump with the valve.

```metadata
pagina: 106
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P106_I1.png
contexto: 
```

![Imagen página 106 - 1](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P106_I1.png)

Slow release valve of blue cable

The end of the hose with a black current limiter is connected to the slow release valve the blue cable.

# Página 107

**Equipo:** Monitor multiparametrico ePM

7-26

7.4 ePM 12/ePM 12A/ePM 12C Host Disassembly

7.4.1 Disassembling Battery Box (Configured)

1. As shown in the following figure, use a Phillips screwdriver to loosen four M3X6 screws, and separate

the battery adapter cable from the extension cable.

2. Remove the battery box component.

3. Pull the connection belt of the battery cover outward to open the battery cover, and put the

screwdriver near the shaft of the battery cover to level the battery cover, and take the battery cover

out.

```metadata
pagina: 107
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P107_I0.png
contexto: 
```

![Imagen página 107 - 0](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P107_I0.png)

```metadata
pagina: 107
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P107_I1.png
contexto: 
```

![Imagen página 107 - 1](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P107_I1.png)

```metadata
pagina: 107
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P107_I2.png
contexto: 
```

![Imagen página 107 - 2](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P107_I2.png)

4. Use the Phillips screwdriver to loosen two M3X6 screws, take the bracket fixing the battery adapter

out, use the Phillips screwdriver to loosen two M3X6 screws, and take the battery adapter out.

```metadata
pagina: 107
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P107_I3.png
contexto: 
```

![Imagen página 107 - 3](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P107_I3.png)

```metadata
pagina: 107
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P107_I4.png
contexto: 
```

![Imagen página 107 - 4](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P107_I4.png)

```metadata
pagina: 107
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P107_I5.png
contexto: 
```

![Imagen página 107 - 5](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P107_I5.png)

```metadata
pagina: 107
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P107_I6.png
contexto: 
```

![Imagen página 107 - 6](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P107_I6.png)

# Página 108

**Equipo:** Monitor multiparametrico ePM

7-27

7.4.2 Disassembling Front/rear Housing Components of Host

1. Use a long Phillips screwdriver to loosen four M4X8 screws.

2. Open the front/rear housings, and remove the display screen connection cable and keypad

connection cable.

Note: During reassembly, close the front/rear covers and pull the cables upward using a hand.

7.4.3 Disassembling Front Housing Component

1. Remove the cable connecting the keypad.

2. Loosen the five ST3.3X8 screws shown in the figure, and take the keypad out.

```metadata
pagina: 108
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P108_I0.png
contexto: 
```

![Imagen página 108 - 0](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P108_I0.png)

Before closing the front/rear covers, pull the cables upward using a hand.

```metadata
pagina: 108
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P108_I1.png
contexto: 
```

![Imagen página 108 - 1](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P108_I1.png)

```metadata
pagina: 108
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P108_I2.png
contexto: 
```

![Imagen página 108 - 2](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P108_I2.png)

```metadata
pagina: 108
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P108_I3.png
contexto: 
```

![Imagen página 108 - 3](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P108_I3.png)

# Página 109

**Equipo:** Monitor multiparametrico ePM

7-28

7.4.4 Disassembling Display Screen and Alarm Indicator

1. Remove the four cable ties from the cables.

2. Remove the cables connecting with the touch screen, display screen, and alarm indicator.

3. Loosen the sticker connecting the touch screen PFC with the sheet metal and the cable stuck to the

sheet metal.

4. Loosen the eight ST3.3X8 screws shown in the figure, and remove the display screen component.

```metadata
pagina: 109
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P109_I0.png
contexto: 
```

![Imagen página 109 - 0](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P109_I0.png)

Loosen the cable connection.

Loosen the FPC sticker.

Loosen the cable sticker.

```metadata
pagina: 109
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P109_I1.png
contexto: 
```

![Imagen página 109 - 1](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P109_I1.png)

Four cable ties

```metadata
pagina: 109
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P109_I2.png
contexto: 
```

![Imagen página 109 - 2](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P109_I2.png)

Five ST3.3X8 screws

Keypad connection cable

# Página 110

**Equipo:** Monitor multiparametrico ePM

7-29

5. Loosen the two M3X6 screws, and take the alarm indicator board out.

6. Loosen the two M3X6 screws with the mark "b" on the right top of the sheet metal.

7. Loosen the two M2X4 screws at the left side of the sheet metal.

8. Loosen the two M2X4 screws at the left side of the sheet metal, and take the display screen out.

9. Loosen the sticker connecting the touch screen with the front housing, and tilt and take the touch

screen out.

```metadata
pagina: 110
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P110_I0.png
contexto: 
```

![Imagen página 110 - 0](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P110_I0.png)

```metadata
pagina: 110
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P110_I1.png
contexto: 
```

![Imagen página 110 - 1](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P110_I1.png)

```metadata
pagina: 110
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P110_I2.png
contexto: 
```

![Imagen página 110 - 2](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P110_I2.png)

Two M2X4 screws Two M2X4 screws

Two M3X6 screws

```metadata
pagina: 110
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P110_I3.png
contexto: 
```

![Imagen página 110 - 3](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P110_I3.png)

```metadata
pagina: 110
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P110_I4.png
contexto: 
```

![Imagen página 110 - 4](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P110_I4.png)

Eight ST3.3X8 screws with the sheet metal mark "a"

# Página 111

**Equipo:** Monitor multiparametrico ePM

7-30

10. Use cutting pliers to cut the binding straps fixing the display screen connection cable and keypad

connection cable, remove the cable from the keypad socket, and remove the display screen

connection cable and keypad connection cable.

Note 1. During reassembly of the touch screen rubber, follow the requirements below to perform

assembly.

```metadata
pagina: 111
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P111_I0.png
contexto: 
```

![Imagen página 111 - 0](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P111_I0.png)

```metadata
pagina: 111
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P111_I1.png
contexto: 
```

![Imagen página 111 - 1](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P111_I1.png)

```metadata
pagina: 111
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P111_I2.png
contexto: 
```

![Imagen página 111 - 2](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P111_I2.png)

When taking the touch screen out, hold the bottom with a hand to support the touch screen up.

Hold the touch screen glass with hand, and do not take the FPC soft chip.

Wash off the double-sided tape.

# Página 112

**Equipo:** Monitor multiparametrico ePM

7-31

Note 2. During reassembly of the touch screen, follow the requirements below to perform assembly.

Note 3. After reassembly of the touch screen, follow the requirements below to press the touch screen.

```metadata
pagina: 112
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P112_I0.png
contexto: 
```

![Imagen página 112 - 0](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P112_I0.png)

Tilt the touch screen, and put it in from the protrusion of the front housing.

When putting the touch screen in, hold the bottom with a hand to support the touch screen up and avoid the touch screen from touching the double-sided tape.

Hold the touch screen glass with hand, and do not take the FPC soft chip.

```metadata
pagina: 112
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P112_I1.png
contexto: 
```

![Imagen página 112 - 1](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P112_I1.png)

```metadata
pagina: 112
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P112_I2.png
contexto: 
```

![Imagen página 112 - 2](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P112_I2.png)

```metadata
pagina: 112
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P112_I3.png
contexto: 
```

![Imagen página 112 - 3](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P112_I3.png)

Amplified

The middle framed hole in the front housing is the display area of the display screen, and so double-sided tape cannot be stuck to this display area.

1. Stick the double-sided tape in alignment with the mark line at the bottom.

2. Stick the double-sided tape in alignment with the mark lines at both outer laterals.

Amplified

Note: The product is configured with a light sensor, so a small hole will be found in this position of the front housing.

Note  ④ . The pit of the top double-sided tape is upward.

Note  ① . The pit of the bottom double-sided tape is upward.  ②  The protrusion of the lateral double-sided tape needs to be put in this pit.

Note  ③ . When sticking the short double-sided tape at the bottom, use the pit position of the long double-sided tape at the bottom as the baseline.

3. Stick the double-sided tape in alignment with the mark line on the top.

# Página 113

**Equipo:** Monitor multiparametrico ePM

7-32

7.4.5 Disassembling WiFi and Parameter Panel

1. Remove cables.

Note. During reassembly, follow the requirements below to perform binding and fixing.

```metadata
pagina: 113
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P113_I0.png
contexto: 
```

![Imagen página 113 - 0](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P113_I0.png)

Penetrate the binding strap through the hole.

Bind the cables of the speaker, WiFi, recorder, rear alarm indicator, gas module, and battery box (optional) using the cables ties.

The cables of the CO2 gas module cable in this two sections must be pulled tight (optional).

The cables of the rear alarm indicator cable in this section must be pulled tight (optional).

```metadata
pagina: 113
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P113_I1.png
contexto: 
```

![Imagen página 113 - 1](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P113_I1.png)

Collect the excessive section of the cables of the rear alarm indicator (optional) and gas module (optional) together using hands.

Insert the rear alarm indicator cable into the slot.

```metadata
pagina: 113
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P113_I2.png
contexto: 
```

![Imagen página 113 - 2](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P113_I2.png)

```metadata
pagina: 113
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P113_I3.png
contexto: 
```

![Imagen página 113 - 3](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P113_I3.png)

Cut binding straps.

Recorder cable (optional)

Rear alarm indicator cable (optional)

Speaker cable

CO2 gas module cable (optional)

```metadata
pagina: 113
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P113_I4.png
contexto: 
```

![Imagen página 113 - 4](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P113_I4.png)

Press the area of the touch screen shown in the figure.

# Página 114

**Equipo:** Monitor multiparametrico ePM

7-33

2. When WiFi is configured, disassemble the WiFi module.

A. Take the WiFi module out.

B. Remove the WiFi cable.

C. Loosen the three M2X4 screws fixing the WiFi module and WiFi load board, and take the WiFi module

and WiFi load board out.

Note. During reassembly of the WiFi module, follow the requirements below to perform assembly.

3. When mainstream CO 2  is configured, disassemble the CO 2  module.

Remove the cables pointed by the arrows in the following figure, loosen three ST3.3X8 cross pan head

tapping screws using the screwdriver, and take the module out.

```metadata
pagina: 114
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P114_I0.png
contexto: 
```

![Imagen página 114 - 0](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P114_I0.png)

```metadata
pagina: 114
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P114_I1.png
contexto: 
```

![Imagen página 114 - 1](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P114_I1.png)

Tilt and insert the WiFi module and press it to the bottom.

Stick the antenna.

Amplified

```metadata
pagina: 114
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P114_I2.png
contexto: 
```

![Imagen página 114 - 2](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P114_I2.png)

Tilt and insert the WiFi module and press it to the bottom.

WiFi cable (optional)

```metadata
pagina: 114
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P114_I3.png
contexto: 
```

![Imagen página 114 - 3](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P114_I3.png)

Fix the WiFi module with the WiFi load board using three M2X4 screws.

Antenna

# Página 115

**Equipo:** Monitor multiparametrico ePM

7-34

4. When microstream CO 2  is configured, disassemble the CO 2  module.

1. Loosen three ST3.3X8 cross pan head tapping screws using the screwdriver, and take the module out.

B. Remove the connection between the microstream module exhaust hose and panel exhaust hose.

Note. During reassembly of the microstream CO 2  module, follow the requirements below to perform

assembly.

```metadata
pagina: 115
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P115_I0.png
contexto: 
```

![Imagen página 115 - 0](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P115_I0.png)

Three ST3.3X8 screws

```metadata
pagina: 115
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P115_I1.png
contexto: 
```

![Imagen página 115 - 1](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P115_I1.png)

Exhaust hose

```metadata
pagina: 115
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P115_I2.png
contexto: 
```

![Imagen página 115 - 2](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P115_I2.png)

Three ST3.3X8 screws

Cable

# Página 116

**Equipo:** Monitor multiparametrico ePM

7-35

5. When sidestream CO 2  is configured, disassemble the CO 2  module.

A. Loosen three ST3.3X8 cross pan head tapping screws using the screwdriver, and loosen the hose of the

sidestream CO 2 .

B. Loosen the cable connection, and take the module out.

```metadata
pagina: 116
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P116_I0.png
contexto: 
```

![Imagen página 116 - 0](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P116_I0.png)

Three ST3.3X8 screws

```metadata
pagina: 116
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P116_I1.png
contexto: 
```

![Imagen página 116 - 1](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P116_I1.png)

Transparent exhaust hose connected with the water tank Condensate hose

Panel exhaust hose

```metadata
pagina: 116
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P116_I2.png
contexto: 
```

![Imagen página 116 - 2](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P116_I2.png)

Three ST3.3X8 screws

The panel cables are wound two circles in this position.

The cables here are set aside to avoid being crushed.

Lead the two exhaust hoses connected with the panel through the module bottom.

# Página 117

**Equipo:** Monitor multiparametrico ePM

7-36

C. Disassemble the two PT2.0X6 screws on the panel water tank, and take the water tank out.

Note. During reassembly of the sidestream CO 2  module, follow the requirements below to perform

assembly.

```metadata
pagina: 117
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P117_I0.png
contexto: 
```

![Imagen página 117 - 0](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P117_I0.png)

Two PT2.0X6 screws

```metadata
pagina: 117
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P117_I1.png
contexto: 
```

![Imagen página 117 - 1](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P117_I1.png)

M02D cable

```metadata
pagina: 117
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P117_I2.png
contexto: 
```

![Imagen página 117 - 2](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P117_I2.png)

Transparent hose Condensate hose

```metadata
pagina: 117
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P117_I3.png
contexto: 
```

![Imagen página 117 - 3](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P117_I3.png)

Cable

# Página 118

**Equipo:** Monitor multiparametrico ePM

7-37

6. Remove the panel cable from the mainboard, and remove the NIBP exhaust hose.

7. Loosen two ST3.3X8 cross pan head tapping screws using the screwdriver, and take the panel fixing

pin and panel component out.

8. When a mainstream module is configured, disassemble the mainstream panel port.

A. Use pliers or tweezers to jack the fastener on the panel, and take the interface board out.

B. Rotate the cable anticlockwise, and remove the CO 2  cable.

C. Remove the plug from the panel.

D. Loosen the M5 screw from the upper right corner of the panel, and take the nozzle out.

```metadata
pagina: 118
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P118_I0.png
contexto: 
```

![Imagen página 118 - 0](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P118_I0.png)

```metadata
pagina: 118
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P118_I1.png
contexto: 
```

![Imagen página 118 - 1](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P118_I1.png)

C.O. cable (optional)

IBP cable (optional)

SpO2 cable

Temp cable

ECG cable

NIBP hose

Two ST3.3X8 screws

```metadata
pagina: 118
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P118_I2.png
contexto: 
```

![Imagen página 118 - 2](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P118_I2.png)

```metadata
pagina: 118
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P118_I3.png
contexto: 
```

![Imagen página 118 - 3](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P118_I3.png)

The transparent exhaust hose connected with the water tank is connected with the nozzle at the left lower side.

Connect the condensate hose to the upper nozzle.

Connect the panel exhaust hose.

The transparent exhaust hose in this position is led through the lateral of the sheet metal.

Lead the condensate hose and panel exhaust hose through the lateral of the sheet metal.

Use three ST3.3X8 screws.

The transparent exhaust hose in this position is led through the lateral of the sheet metal.

The cable and condensate hose connected with the mainboard are led from the top.

The condensate hose is wound one circle in this position and inserted into the slot.

# Página 119

**Equipo:** Monitor multiparametrico ePM

7-38

Note 1. During reassembly, the interface board of the mainstream panel should be in the following

direction.

Note 2. During reassembly of the cable to the interface board, tighten it firmly anticlockwise.

9. When an microstream module is configured, disassemble the microstream water tank.

A. Use pliers or tweezers to jack the fastener on the panel, and take the microstream water tank base out.

B. Loosen the M5 screw from the upper right corner of the panel, and take the exhaust nozzle out.

C. Use tweezers to loosen the fastener on the water tank base, and take the microstream connector out.

```metadata
pagina: 119
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P119_I0.png
contexto: 
```

![Imagen página 119 - 0](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P119_I0.png)

Rotate the signal cable fastener anticlockwise to stick to this position.

```metadata
pagina: 119
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P119_I1.png
contexto: 
```

![Imagen página 119 - 1](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P119_I1.png)

```metadata
pagina: 119
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P119_I2.png
contexto: 
```

![Imagen página 119 - 2](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P119_I2.png)

Protrusion upward

Amplified

```metadata
pagina: 119
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P119_I3.png
contexto: 
```

![Imagen página 119 - 3](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P119_I3.png)

```metadata
pagina: 119
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P119_I4.png
contexto: 
```

![Imagen página 119 - 4](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P119_I4.png)

```metadata
pagina: 119
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P119_I5.png
contexto: 
```

![Imagen página 119 - 5](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P119_I5.png)

```metadata
pagina: 119
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P119_I6.png
contexto: 
```

![Imagen página 119 - 6](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P119_I6.png)

Plug Nipple Nut

# Página 120

**Equipo:** Monitor multiparametrico ePM

7-39

10. When a sidestream module is configured, disassemble the sidestream water tank.

A. Remove the cable or hose from the water tank.

B. Remove the exhaust hose from the panel, loosen the M4 screw on the exhaust nozzle, and take the

nozzle out.

C. Loosen the M5 screw/M4 nut on the panel, and take the exhaust nozzle out.

D. Loosen the four PT2.0X6 screws on the panel, and take the bracket of the sidestream water tank out.

11. Disassemble the panel cable.

A. According to the figure, rotate different parameter cables anticlockwise, and remove them.

B. Take the arrival reminding shrapnel out.

```metadata
pagina: 120
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P120_I0.png
contexto: 
```

![Imagen página 120 - 0](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P120_I0.png)

M02D cable

```metadata
pagina: 120
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P120_I1.png
contexto: 
```

![Imagen página 120 - 1](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P120_I1.png)

Transparent hose Condensate hose

```metadata
pagina: 120
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P120_I2.png
contexto: 
```

![Imagen página 120 - 2](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P120_I2.png)

M4 nut and exhaust nozzle

```metadata
pagina: 120
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P120_I3.png
contexto: 
```

![Imagen página 120 - 3](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P120_I3.png)

```metadata
pagina: 120
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P120_I4.png
contexto: 
```

![Imagen página 120 - 4](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P120_I4.png)

Nipple Nut

```metadata
pagina: 120
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P120_I5.png
contexto: 
```

![Imagen página 120 - 5](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P120_I5.png)

Loosen fastener.

# Página 121

**Equipo:** Monitor multiparametrico ePM

7-40

Note. During reassembly, follow the requirements below to perform cable assembling.

```metadata
pagina: 121
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P121_I0.png
contexto: 
```

![Imagen página 121 - 0](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P121_I0.png)

Optional: IBP cable 1 channel (black)

Optional: IBP cable 2 channel (gray)

Temp 1 channel (red)

Temp 2 channel (blue)

Diagram (CO2 gas module is used)

Optional: C.O. cable

SpO2 cable ECG cable

```metadata
pagina: 121
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P121_I1.png
contexto: 
```

![Imagen página 121 - 1](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P121_I1.png)

When the IBP function is selected

Disassemble the arrival reminding shrapnel.

Shrapnel Shrapnel

When the C.O. function is selected

```metadata
pagina: 121
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P121_I2.png
contexto: 
```

![Imagen página 121 - 2](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P121_I2.png)

Optional: C.O. cable ECG cable

SpO2 cable

Optional: IBP cable 1 channel (black)

Optional: IBP cable 2 channel (gray)

Temp 1 channel (red)

Temp 2 channel (blue)

Diagram (CO2 gas module is not used)

```metadata
pagina: 121
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P121_I3.png
contexto: 
```

![Imagen página 121 - 3](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P121_I3.png)

When the IBP function is selected

C.O. function

Disassemble the arrival reminding shrapnel.

Shrapnel

Shrapnel

# Página 122

**Equipo:** Monitor multiparametrico ePM

7-41

12. Disassemble the NIBP nozzle: Rotate the NIBP nozzle anticlockwise, and disassemble the NIBP nozzle.

7.4.6 Disassembling Gas Module

1. When mainstream CO 2  is configured:

A. Loosen the three M3X6 screws in the figure, and take the mainstream CO 2  isolation power board out.

B. Remove the cable connecting the mainstream isolation power board with the mainboard.

2. When microstream CO 2  is configured:

A. Remove the cable connecting the microstream CO 2  module with the adapter.

B. Remove the cable connecting the mainboard.

C. Loosen the four M3X6 screws in the figure, and take the microstream CO 2  module out.

D. Loosen the three M3X6 screws, and take the adapter out.

```metadata
pagina: 122
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P122_I0.png
contexto: 
```

![Imagen página 122 - 0](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P122_I0.png)

Use three M3X6 screws.

Cable

```metadata
pagina: 122
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P122_I1.png
contexto: 
```

![Imagen página 122 - 1](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P122_I1.png)

```metadata
pagina: 122
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P122_I2.png
contexto: 
```

![Imagen página 122 - 2](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P122_I2.png)

Diagram (CO2 module is not configured)

Diagram (CO2 module is configured)

NIBP nozzle component

```metadata
pagina: 122
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P122_I3.png
contexto: 
```

![Imagen página 122 - 3](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P122_I3.png)

```metadata
pagina: 122
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P122_I4.png
contexto: 
```

![Imagen página 122 - 4](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P122_I4.png)

```metadata
pagina: 122
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P122_I5.png
contexto: 
```

![Imagen página 122 - 5](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P122_I5.png)

Rotate the temp socket anticlockwise and stick it to the locating slot.

Rotate other sockets anticlockwise and stick them to the locating slot.

Cable connector assembly diagram

# Página 123

**Equipo:** Monitor multiparametrico ePM

7-42

3. When sidestream CO 2  is configured:

A. Loosen the two M3X6 screws in the figure, and take the sidestream gas module out.

B. Take the air filter and short-circuited hose out.

C. Loosen the three M2.5X4 countersunk screws, and take the cover out.

D. Take the silicone case out.

7.4.7 Disassembling Recorder/Recorder Bracket

1. When the recorder is configured, disassemble the recorder:

A. Loosen the two M3X6 screws of the recorder, loosen the two fasteners of the recorder, and take the

recorder out.

B. Remove the cable connecting the two sockets of the recorder.

```metadata
pagina: 123
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P123_I0.png
contexto: 
```

![Imagen página 123 - 0](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P123_I0.png)

Air filter

Short-circuited hose

```metadata
pagina: 123
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P123_I1.png
contexto: 
```

![Imagen página 123 - 1](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P123_I1.png)

Three M2.5X4 screws

Cover

```metadata
pagina: 123
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P123_I2.png
contexto: 
```

![Imagen página 123 - 2](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P123_I2.png)

Take the silicone case out.

```metadata
pagina: 123
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P123_I3.png
contexto: 
```

![Imagen página 123 - 3](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P123_I3.png)

Use two M3X6 screws.

```metadata
pagina: 123
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P123_I4.png
contexto: 
```

![Imagen página 123 - 4](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P123_I4.png)

```metadata
pagina: 123
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P123_I5.png
contexto: 
```

![Imagen página 123 - 5](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P123_I5.png)

Four M3X6 screws

Cable connecting the mainboard

Cable connecting the microstream CO2 module with the adapter

Three M3X6 screws

# Página 124

**Equipo:** Monitor multiparametrico ePM

7-43

2. Take the recorder bracket out: Loosen the two ST3.3X8 screws on the recorder bracket, and take the

recorder bracket out.

7.4.8 Disassembling Main Bracket Component

1. When the battery box is configured, remove the cable connecting the battery box.

2. Loosen the battery cover.

```metadata
pagina: 124
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P124_I0.png
contexto: 
```

![Imagen página 124 - 0](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P124_I0.png)

Take out from the hole at the bottom of the rear housing.

Penetrate the hole of the sheet metal.

```metadata
pagina: 124
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P124_I1.png
contexto: 
```

![Imagen página 124 - 1](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P124_I1.png)

Two ST3.3X8 screws

Recorder bracket

```metadata
pagina: 124
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P124_I2.png
contexto: 
```

![Imagen página 124 - 2](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P124_I2.png)

Two M3X6 screws

Fastener Fastener

```metadata
pagina: 124
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P124_I3.png
contexto: 
```

![Imagen página 124 - 3](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P124_I3.png)

Insert and connect recorder cable.

# Página 125

**Equipo:** Monitor multiparametrico ePM

7-44

3. Loosen the five ST3.3X8 screws shown in the figure, and remove the main bracket component.

Note 1. Before reassembling the main bracket component, insert the connection belt of the battery cover

to the locating post of the rear housing shown in the following figure.

Note 2. Before closing the battery cover, switch the battery to the vertical position shown in the figure.

```metadata
pagina: 125
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P125_I0.png
contexto: 
```

![Imagen página 125 - 0](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P125_I0.png)

After the battery is switched to the vertical position, close the battery cover.

```metadata
pagina: 125
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P125_I1.png
contexto: 
```

![Imagen página 125 - 1](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P125_I1.png)

```metadata
pagina: 125
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P125_I2.png
contexto: 
```

![Imagen página 125 - 2](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P125_I2.png)

Put the battery cover aside, without closing it.

Amplified

Insert the connection belt to the locating post of the rear housing.

```metadata
pagina: 125
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P125_I3.png
contexto: 
```

![Imagen página 125 - 3](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P125_I3.png)

Open the battery cover.

```metadata
pagina: 125
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P125_I4.png
contexto: 
```

![Imagen página 125 - 4](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P125_I4.png)

Five ST3.3X8 screws

# Página 126

**Equipo:** Monitor multiparametrico ePM

7-45

7.4.9 Disassembling Speaker

1. Loosen the two ST3.3X8 screws of the speaker component shown in the figure, and take the speaker

component out.

7.4.10 Disassembling Rear Alarm Indicator (Configured)

1. Loosen the eight ST3.3X8 screws on the cover component shown in the figure, and take the top cover

component out.

2. Loosen the one ST3.3X8 screw on the rear alarm indicator shown in the figure, and take the rear alarm

indicator component out.

7.4.11 Disassembling Power Module

1. Remove the AC input cable, and remove the cable connecting the power module with mainboard

out.

2. Loosen the four M3X6 screws of the power module, and take the power module out.

```metadata
pagina: 126
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P126_I0.png
contexto: 
```

![Imagen página 126 - 0](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P126_I0.png)

AC input cable

Cable connecting the mainboards

```metadata
pagina: 126
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P126_I1.png
contexto: 
```

![Imagen página 126 - 1](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P126_I1.png)

Four M3X6 screws

```metadata
pagina: 126
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P126_I2.png
contexto: 
```

![Imagen página 126 - 2](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P126_I2.png)

Two ST3.3X8 screws

```metadata
pagina: 126
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P126_I3.png
contexto: 
```

![Imagen página 126 - 3](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P126_I3.png)

# Página 127

**Equipo:** Monitor multiparametrico ePM

7-46

7.4.12 Disassembling SpO 2  Module (When Nellcor/Massimo SpO 2  Is Configured)

1. When Nellcor SpO 2  is configured:

Loosen the one M2X4 screw on the Nellcor SpO 2 , and take the Nellcor SpO 2  board out.

2. When Massimo SpO 2  is configured:

Loosen the two M2X4 screws on the Massimo SpO 2 , and take the Massimo SpO 2  board and insulation

sheet out.

7.4.13 Disassembling C.O. Board (Configured)

1. Remove the cable connecting the C.O. board with the mainboard.

2. Loosen the two M3X6 screws on the Massimo SpO 2 , and take the C.O. board and insulation sheet out.

```metadata
pagina: 127
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P127_I0.png
contexto: 
```

![Imagen página 127 - 0](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P127_I0.png)

Assemble Massimo SpO 2  board.

Use two M3X6 screws.

```metadata
pagina: 127
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P127_I1.png
contexto: 
```

![Imagen página 127 - 1](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P127_I1.png)

SpO 2  board insulation sheet

```metadata
pagina: 127
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P127_I2.png
contexto: 
```

![Imagen página 127 - 2](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P127_I2.png)

One M2X4 screw

Assemble Nellcor SpO 2  board.

# Página 128

**Equipo:** Monitor multiparametrico ePM

7-47

7.4.14 Disassembling Mainboard

1. Remove the pump/valve connection cables from the mainboard.

2. Take the two interfaces of the NIBP hose from the mainboard sensor.

3. Remove the connection cable of the battery adapter from the mainboard.

4. Loosen the six M3X6 screws from the main bracket in the figure.

5. Loosen the two screws on the rear of the main bracket sheet metal, and take the mainboard out.

```metadata
pagina: 128
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P128_I0.png
contexto: 
```

![Imagen página 128 - 0](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P128_I0.png)

Two connection cables of the battery adapter

```metadata
pagina: 128
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P128_I1.png
contexto: 
```

![Imagen página 128 - 1](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P128_I1.png)

Gas pump connection cable Gas valve connection cable

Two interfaces connecting the NIBP hose and mainboard sensor

```metadata
pagina: 128
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P128_I2.png
contexto: 
```

![Imagen página 128 - 2](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P128_I2.png)

C.O. board Black insulation sheet

Three M3X6 screws

Connection cable

# Página 129

**Equipo:** Monitor multiparametrico ePM

7-48

6. As shown in the following figure, loosen the nuts or screws on the rear of the mainboard, and take

the studs out.

7.4.15 Disassembling Power Adapter and NIBP Pump/Valve

1. As shown in the following figure, loosen the two ST3.3X8 screws, and take the battery adapter out.

```metadata
pagina: 129
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P129_I0.png
contexto: 
```

![Imagen página 129 - 0](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P129_I0.png)

```metadata
pagina: 129
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P129_I1.png
contexto: 
```

![Imagen página 129 - 1](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P129_I1.png)

```metadata
pagina: 129
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P129_I2.png
contexto: 
```

![Imagen página 129 - 2](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P129_I2.png)

When the C.O. function is selected, there are three M3 nuts here.

When the Masimo SpO 2  is selected, there are two M3 nuts here.

When the Nellcor SpO 2  is selected, there is one M2X4 screw here.

When the C.O. function is selected, there are three studs here.

When the Masimo SpO 2  is selected, there are two studs here.

When the Nellcor SpO 2  is selected, there is one stud here.

```metadata
pagina: 129
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P129_I3.png
contexto: 
```

![Imagen página 129 - 3](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P129_I3.png)

Two screws

```metadata
pagina: 129
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P129_I4.png
contexto: 
```

![Imagen página 129 - 4](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P129_I4.png)

Six M3X6 screws

# Página 130

**Equipo:** Monitor multiparametrico ePM

7-49

2. Loosen the hose connecting the NIBP pump/valve.

3. Loosen the fastener fixing the NIBP valve, and take the NIBP valve out.

4. Loosen the two binding straps fixing the NIBP pump, and take the NIBP pump out.

Note: During reassembly, ensure that the hose is correctly connected with the quick/slow release valve.

```metadata
pagina: 130
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P130_I0.png
contexto: 
```

![Imagen página 130 - 0](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P130_I0.png)

Slow release valve of blue cable

The end of the hose with a black current limiter is connected to the slow release valve the blue cable.

```metadata
pagina: 130
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P130_I1.png
contexto: 
```

![Imagen página 130 - 1](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P130_I1.png)

Two binding straps

Loosen the fastener fixing the NIBP valve.

Loose the hose connecting the pump with the valve.

# Página 131

**Equipo:** Monitor multiparametrico ePM

7-50

7.5 ePM 10/ePM 10A/ePM 10C Host Disassembly

7.5.1 Disassembling Front/rear Housing Components of Host

1. Use a Phillips screwdriver to loosen four M4X8 screws.

2. Open the front/rear housings, and remove the display screen connection cable and keypad

connection cable.

Note: During reassembly, close the front/rear covers and pull the cables upward using a hand.

```metadata
pagina: 131
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P131_I0.png
contexto: 
```

![Imagen página 131 - 0](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P131_I0.png)

Before closing the front/rear covers, pull the cables upward using a hand.

```metadata
pagina: 131
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P131_I1.png
contexto: 
```

![Imagen página 131 - 1](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P131_I1.png)

```metadata
pagina: 131
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P131_I2.png
contexto: 
```

![Imagen página 131 - 2](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P131_I2.png)

```metadata
pagina: 131
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P131_I3.png
contexto: 
```

![Imagen página 131 - 3](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P131_I3.png)

```metadata
pagina: 131
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P131_I4.png
contexto: 
```

![Imagen página 131 - 4](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P131_I4.png)

Four M4X8 screws

# Página 132

**Equipo:** Monitor multiparametrico ePM

7-51

7.5.2 Disassembling Keypad

1. Remove the cable connecting the keypad.

2. Loosen the five ST3.3X8 screws shown in the figure, and take the keypad out.

7.5.3 Disassembling Display Screen and Alarm Indicator

1. Remove the cables connecting with the touch screen, display screen, and alarm indicator.

2. Remove the five cable ties from cables, and loosen the cables stuck to the sheet metal.

3. Loosen the sticker connecting the touch screen PFC with the sheet metal.

```metadata
pagina: 132
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P132_I0.png
contexto: 
```

![Imagen página 132 - 0](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P132_I0.png)

Loosen the cable connection.

```metadata
pagina: 132
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P132_I1.png
contexto: 
```

![Imagen página 132 - 1](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P132_I1.png)

Five ST3.3X8 screws

Keypad connection cable

# Página 133

**Equipo:** Monitor multiparametrico ePM

7-52

4. Loosen the eight ST3.3X8 screws shown in the figure, and remove the display screen component.

5. Loosen the two M3X6 screws, and take the alarm indicator board out.

6. Loosen the two M3X6 screws with the mark "b" on the right top of the sheet metal.

7. Loosen the two M2X4 screws at the left side of the sheet metal.

8. Loosen the two M2X4 screws at the left side of the sheet metal, and take the display screen out.

```metadata
pagina: 133
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P133_I0.png
contexto: 
```

![Imagen página 133 - 0](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P133_I0.png)

```metadata
pagina: 133
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P133_I1.png
contexto: 
```

![Imagen página 133 - 1](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P133_I1.png)

Eight ST3.3X8 screws with the sheet metal mark "a"

```metadata
pagina: 133
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P133_I2.png
contexto: 
```

![Imagen página 133 - 2](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P133_I2.png)

Loosen the cable sticker.

Five cable ties

Loosen the FPC sticker.

# Página 134

**Equipo:** Monitor multiparametrico ePM

7-53

9. Loosen the sticker connecting the touch screen with the front housing, and tilt and take the touch

screen out.

Note 1. During reassembly of the touch screen rubber, follow the requirements below to perform

assembly.

```metadata
pagina: 134
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P134_I0.png
contexto: 
```

![Imagen página 134 - 0](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P134_I0.png)

```metadata
pagina: 134
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P134_I1.png
contexto: 
```

![Imagen página 134 - 1](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P134_I1.png)

When taking the touch screen out, hold the bottom with a hand to support the touch screen up.

Hold the touch screen glass with hand, and do not take the FPC soft chip.

Wash off the double-sided tape.

```metadata
pagina: 134
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P134_I2.png
contexto: 
```

![Imagen página 134 - 2](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P134_I2.png)

```metadata
pagina: 134
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P134_I3.png
contexto: 
```

![Imagen página 134 - 3](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P134_I3.png)

Two M2X4 screws

```metadata
pagina: 134
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P134_I4.png
contexto: 
```

![Imagen página 134 - 4](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P134_I4.png)

Two M2X4 screws

Two M3X6 screws

# Página 135

**Equipo:** Monitor multiparametrico ePM

7-54

Note 2. During reassembly of the touch screen, follow the requirements below to perform assembly.

Note 3. After reassembly of the touch screen, follow the requirements below to press the touch screen.

```metadata
pagina: 135
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P135_I0.png
contexto: 
```

![Imagen página 135 - 0](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P135_I0.png)

Tilt the touch screen, and put it in from the protrusion of the front housing.

When putting the touch screen in, hold the bottom with a hand to support the touch screen up and avoid the touch screen from touching the double-sided tape.

Hold the touch screen glass with hand, and do not take the FPC soft chip.

```metadata
pagina: 135
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P135_I1.png
contexto: 
```

![Imagen página 135 - 1](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P135_I1.png)

```metadata
pagina: 135
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P135_I2.png
contexto: 
```

![Imagen página 135 - 2](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P135_I2.png)

```metadata
pagina: 135
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P135_I3.png
contexto: 
```

![Imagen página 135 - 3](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P135_I3.png)

Amplified

The middle framed hole in the front housing is the display area of the display screen, and so double-sided tape cannot be stuck to this display area.

1. Stick the double-sided tape in alignment with the mark line at the bottom.

2. Stick the double-sided tape in alignment with the mark lines at both outer laterals.

Amplified

Note: The product is configured with a light sensor, so a small hole will be found in this position of the front housing.

Note  ④ . The pit of the top double-sided tape is upward.

Note  ① . The pit of the bottom double-sided tape is upward.  ②  The protrusion of the lateral double-sided tape needs to be put in this pit.

Note  ③ . When sticking the short double-sided tape at the bottom, use the pit position of the long double-sided tape at the bottom as the baseline.

3. Stick the double-sided tape in alignment with the mark line on the top.

# Página 136

**Equipo:** Monitor multiparametrico ePM

7-55

7.5.4 Disassembling WiFi and Parameter Panel

1. Remove cables.

Note. During reassembly, follow the requirements below to perform binding and fixing.

```metadata
pagina: 136
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P136_I0.png
contexto: 
```

![Imagen página 136 - 0](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P136_I0.png)

Penetrate the binding strap through the hole.

Bind the cables of the speaker, WiFi, recorder, rear alarm indicator, gas module, and battery box (optional) using the cables ties.

The cables of the CO2 gas module cable in this two sections must be pulled tight (optional).

The cables of the rear alarm indicator cable in this section must be pulled tight (optional).

```metadata
pagina: 136
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P136_I1.png
contexto: 
```

![Imagen página 136 - 1](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P136_I1.png)

Collect the excessive section of the cables of the rear alarm indicator (optional) and gas module (optional) together using hands.

Insert the rear alarm indicator cable into the slot.

```metadata
pagina: 136
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P136_I2.png
contexto: 
```

![Imagen página 136 - 2](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P136_I2.png)

```metadata
pagina: 136
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P136_I3.png
contexto: 
```

![Imagen página 136 - 3](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P136_I3.png)

Cut binding straps.

Recorder cable (optional)

Rear alarm indicator cable (optional)

Speaker cable

CO2 gas module cable (optional)

```metadata
pagina: 136
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P136_I4.png
contexto: 
```

![Imagen página 136 - 4](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P136_I4.png)

Press the orange area of the touch screen.

# Página 137

**Equipo:** Monitor multiparametrico ePM

7-56

2. When WiFi is configured, disassemble the WiFi module.

A. Take the WiFi module out.

B. Remove the WiFi cable.

C. Loosen the three M2X4 screws fixing the WiFi module and WiFi load board, and take the WiFi module

and WiFi load board out.

Note. During reassembly of the WiFi module, follow the requirements below to perform assembly.

3. When mainstream CO 2  is configured, disassemble the CO 2  module.

Remove the cables pointed by the arrows in the following figure, loosen three ST3.3X8 cross pan head

tapping screws using the screwdriver, and take the module out.

```metadata
pagina: 137
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P137_I0.png
contexto: 
```

![Imagen página 137 - 0](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P137_I0.png)

```metadata
pagina: 137
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P137_I1.png
contexto: 
```

![Imagen página 137 - 1](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P137_I1.png)

Tilt and insert the WiFi module and press it to the bottom.

Stick the antenna.

Amplified

Insert the antenna into the slot.

```metadata
pagina: 137
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P137_I2.png
contexto: 
```

![Imagen página 137 - 2](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P137_I2.png)

Tilt and insert the WiFi module and press it to the bottom.

WiFi cable (optional)

```metadata
pagina: 137
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P137_I3.png
contexto: 
```

![Imagen página 137 - 3](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P137_I3.png)

Fix the WiFi module with the WiFi load board using three M2X4 screws.

Antenna

# Página 138

**Equipo:** Monitor multiparametrico ePM

7-57

4. When microstream CO 2  is configured, disassemble the CO 2  module.

A. Loosen three ST3.3X8 cross pan head tapping screws using the screwdriver, and take the module out.

B. Remove the connection between the microstream module exhaust hose and panel exhaust hose.

Note. During reassembly of the microstream CO 2  module, follow the requirements below to perform

assembly.

```metadata
pagina: 138
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P138_I0.png
contexto: 
```

![Imagen página 138 - 0](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P138_I0.png)

Three ST3.3X8 screws

The panel cables are wound two circles in this position.

The cables here are set aside to avoid being crushed.

Lead the two exhaust hoses connected with the panel through the module bottom.

```metadata
pagina: 138
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P138_I1.png
contexto: 
```

![Imagen página 138 - 1](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P138_I1.png)

```metadata
pagina: 138
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P138_I2.png
contexto: 
```

![Imagen página 138 - 2](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P138_I2.png)

Three ST3.3X8 screws Exhaust hose

```metadata
pagina: 138
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P138_I3.png
contexto: 
```

![Imagen página 138 - 3](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P138_I3.png)

Three ST3.3X8 screws

Cable

# Página 139

**Equipo:** Monitor multiparametrico ePM

7-58

5. When sidestream CO 2  is configured, disassemble the CO 2  module.

A. Loosen three ST3.3X8 cross pan head tapping screws using the screwdriver, and loosen the hose of the

sidestream CO 2 .

B. Loosen the cable connection, and take the module out.

C. Disassemble the two PT2.0X6 screws on the panel water tank, and take the water tank out.

```metadata
pagina: 139
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P139_I0.png
contexto: 
```

![Imagen página 139 - 0](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P139_I0.png)

Cable

```metadata
pagina: 139
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P139_I1.png
contexto: 
```

![Imagen página 139 - 1](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P139_I1.png)

Three ST3.3X8 screws

```metadata
pagina: 139
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P139_I2.png
contexto: 
```

![Imagen página 139 - 2](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P139_I2.png)

Transparent exhaust hose connected with the water tank Condensate hose

Panel exhaust hose

# Página 140

**Equipo:** Monitor multiparametrico ePM

7-59

Note. During reassembly of the sidestream CO 2  module, follow the requirements below to perform

assembly.

6. Remove the panel cable from the mainboard, and remove the NIBP exhaust hose.

7. Loosen two ST3.3X8 cross pan head tapping screws using the screwdriver, and take the panel fixing

pin and panel component out.

```metadata
pagina: 140
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P140_I0.png
contexto: 
```

![Imagen página 140 - 0](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P140_I0.png)

```metadata
pagina: 140
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P140_I1.png
contexto: 
```

![Imagen página 140 - 1](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P140_I1.png)

The transparent exhaust hose connected with the water tank is connected with the nozzle at the left lower side.

Connect the condensate hose to the upper nozzle.

Connect the panel exhaust hose.

The transparent exhaust hose in this position is led through the lateral of the sheet metal.

Lead the condensate hose and panel exhaust hose through the lateral of the sheet metal.

Use three ST3.3X8 screws.

The transparent exhaust hose in this position is led through the lateral of the sheet metal.

The cable and condensate hose connected with the mainboard are led from the top.

The condensate hose is wound one circle in this position and inserted into the slot.

```metadata
pagina: 140
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P140_I2.png
contexto: 
```

![Imagen página 140 - 2](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P140_I2.png)

Two PT2.0X6 screws

```metadata
pagina: 140
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P140_I3.png
contexto: 
```

![Imagen página 140 - 3](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P140_I3.png)

M02D cable

```metadata
pagina: 140
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P140_I4.png
contexto: 
```

![Imagen página 140 - 4](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P140_I4.png)

Transparent hose Condensate hose

# Página 141

**Equipo:** Monitor multiparametrico ePM

7-60

8. When a mainstream module is configured, disassemble the mainstream panel port.

A. Use pliers or tweezers to jack the fastener on the panel, and take the interface board out.

B. Rotate the cable anticlockwise, and remove the CO 2  cable.

C. Remove the plug from the panel.

D. Loosen the M5 screw from the upper right corner of the panel, and take the nozzle out.

Note 1. During reassembly, the interface board of the mainstream panel should be in the following

direction.

```metadata
pagina: 141
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P141_I0.png
contexto: 
```

![Imagen página 141 - 0](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P141_I0.png)

```metadata
pagina: 141
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P141_I1.png
contexto: 
```

![Imagen página 141 - 1](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P141_I1.png)

```metadata
pagina: 141
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P141_I2.png
contexto: 
```

![Imagen página 141 - 2](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P141_I2.png)

```metadata
pagina: 141
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P141_I3.png
contexto: 
```

![Imagen página 141 - 3](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P141_I3.png)

Plug Nipple Nut

```metadata
pagina: 141
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P141_I4.png
contexto: 
```

![Imagen página 141 - 4](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P141_I4.png)

```metadata
pagina: 141
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P141_I5.png
contexto: 
```

![Imagen página 141 - 5](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P141_I5.png)

C.O. cable (optional)

IBP cable (optional)

SpO2 cable

Temp cable

ECG cable

NIBP hose

Two ST3.3X8 screws

# Página 142

**Equipo:** Monitor multiparametrico ePM

7-61

Note 2. During reassembly of the cable to the interface board, tighten it firmly anticlockwise.

9. When an microstream module is configured, disassemble the microstream water tank.

A. Use pliers or tweezers to jack the fastener on the panel, and take the microstream water tank base out.

B. Loosen the M5 screw from the upper right corner of the panel, and take the exhaust nozzle out.

C. Use tweezers to loosen the fastener on the water tank base, and take the microstream connector out.

```metadata
pagina: 142
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P142_I0.png
contexto: 
```

![Imagen página 142 - 0](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P142_I0.png)

Nipple Nut

```metadata
pagina: 142
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P142_I1.png
contexto: 
```

![Imagen página 142 - 1](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P142_I1.png)

Loosen fastener.

```metadata
pagina: 142
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P142_I2.png
contexto: 
```

![Imagen página 142 - 2](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P142_I2.png)

Rotate the signal cable fastener anticlockwise to stick to this position.

```metadata
pagina: 142
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P142_I3.png
contexto: 
```

![Imagen página 142 - 3](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P142_I3.png)

```metadata
pagina: 142
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P142_I4.png
contexto: 
```

![Imagen página 142 - 4](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P142_I4.png)

Protrusion upward

Amplified

# Página 143

**Equipo:** Monitor multiparametrico ePM

7-62

10. When a sidestream module is configured, disassemble the sidestream water tank.

A. Remove the cable or hose from the water tank.

B. Remove the exhaust hose from the panel, loosen the M4 screw on the exhaust nozzle, and take the

nozzle out.

C. Loosen the M5 screw/M4 nut on the panel, and take the exhaust nozzle out.

D. Loosen the four PT2.0X6 screws on the panel, and take the bracket of the sidestream water tank out.

11. Disassemble the panel cable.

A. According to the figure, rotate different parameter cables anticlockwise, and remove them.

B. Take the arrival reminding shrapnel out.

```metadata
pagina: 143
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P143_I0.png
contexto: 
```

![Imagen página 143 - 0](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P143_I0.png)

Optional: C.O. cable ECG cable

SpO2 cable

Optional: IBP cable 1 channel (black)

Optional: IBP cable 2 channel (gray)

Temp 1 channel (red)

Temp 2 channel (blue)

Diagram (CO2 gas module is not used)

```metadata
pagina: 143
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P143_I1.png
contexto: 
```

![Imagen página 143 - 1](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P143_I1.png)

When the IBP function is selected

C.O. function

Disassemble the arrival reminding shrapnel.

Shrapnel

Shrapnel

```metadata
pagina: 143
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P143_I2.png
contexto: 
```

![Imagen página 143 - 2](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P143_I2.png)

M02D cable

```metadata
pagina: 143
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P143_I3.png
contexto: 
```

![Imagen página 143 - 3](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P143_I3.png)

Transparent hose Condensate hose

```metadata
pagina: 143
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P143_I4.png
contexto: 
```

![Imagen página 143 - 4](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P143_I4.png)

M4 nut and exhaust nozzle

```metadata
pagina: 143
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P143_I5.png
contexto: 
```

![Imagen página 143 - 5](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P143_I5.png)

# Página 144

**Equipo:** Monitor multiparametrico ePM

7-63

Note. During reassembly, follow the requirements below to perform cable assembling.

12. Disassemble the NIBP nozzle: Rotate the NIBP nozzle anticlockwise, and disassemble the NIBP nozzle.

```metadata
pagina: 144
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P144_I0.png
contexto: 
```

![Imagen página 144 - 0](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P144_I0.png)

```metadata
pagina: 144
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P144_I1.png
contexto: 
```

![Imagen página 144 - 1](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P144_I1.png)

Diagram (CO2 module is not configured)

Diagram (CO2 module is configured)

NIBP nozzle component

```metadata
pagina: 144
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P144_I2.png
contexto: 
```

![Imagen página 144 - 2](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P144_I2.png)

```metadata
pagina: 144
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P144_I3.png
contexto: 
```

![Imagen página 144 - 3](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P144_I3.png)

```metadata
pagina: 144
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P144_I4.png
contexto: 
```

![Imagen página 144 - 4](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P144_I4.png)

Rotate the temp socket anticlockwise and stick it to the locating slot.

Rotate other sockets anticlockwise and stick them to the locating slot.

Cable connector assembly diagram

```metadata
pagina: 144
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P144_I5.png
contexto: 
```

![Imagen página 144 - 5](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P144_I5.png)

Optional: IBP cable 1 channel (black)

Optional: IBP cable 2 channel (gray)

Temp 1 channel (red)

Temp 2 channel (blue)

Diagram (CO2 gas module is used)

Optional: C.O. cable

SpO2 cable ECG cable

```metadata
pagina: 144
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P144_I6.png
contexto: 
```

![Imagen página 144 - 6](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P144_I6.png)

When the IBP function is selected

Disassemble the arrival reminding shrapnel.

Shrapnel Shrapnel

When the C.O. function is selected

# Página 145

**Equipo:** Monitor multiparametrico ePM

7-64

7.5.5 Disassembling Gas Module

1. When mainstream CO 2  is configured:

A. Loosen the three M3X6 screws in the figure, and take the mainstream CO 2  isolation power board out.

B. Remove the cable connecting the mainstream isolation power board with the mainboard.

2. When microstream CO 2  is configured:

A. Remove the cable connecting the microstream CO 2  module with the adapter.

B. Remove the cable connecting the mainboard.

C. Loosen the four M3X6 screws in the figure, and take the microstream CO 2  module out.

D. Loosen the three M3X6 screws, and take the adapter out.

3. When sidestream CO 2  is configured:

A. Loosen the two M3X6 screws in the figure, and take the sidestream gas module out.

B. Take the air filter and short-circuited hose out.

```metadata
pagina: 145
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P145_I0.png
contexto: 
```

![Imagen página 145 - 0](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P145_I0.png)

Use two M3X6 screws.

```metadata
pagina: 145
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P145_I1.png
contexto: 
```

![Imagen página 145 - 1](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P145_I1.png)

```metadata
pagina: 145
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P145_I2.png
contexto: 
```

![Imagen página 145 - 2](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P145_I2.png)

Four M3X6 screws

Cable connecting the mainboard

Cable connecting the microstream CO2 module with the adapter

Three M3X6 screws

```metadata
pagina: 145
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P145_I3.png
contexto: 
```

![Imagen página 145 - 3](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P145_I3.png)

Use three M3X6 screws.

Cable

# Página 146

**Equipo:** Monitor multiparametrico ePM

7-65

C. Loosen the three M2.5X4 countersunk screws, and take the cover out.

D. Take the silicone case out.

7.5.6 Disassembling Recorder/Recorder Bracket

1. When the recorder is configured, disassemble the recorder:

A. Loosen the two M3X6 screws of the recorder, loosen the two fasteners of the recorder, and take the

recorder out.

B. Remove the cable connecting the two sockets of the recorder.

2. Take the recorder bracket out: Loosen the two ST3.3X8 screws on the recorder bracket, and take the

recorder bracket out.

```metadata
pagina: 146
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P146_I0.png
contexto: 
```

![Imagen página 146 - 0](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P146_I0.png)

Two ST3.3X8 screws

Recorder bracket

```metadata
pagina: 146
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P146_I1.png
contexto: 
```

![Imagen página 146 - 1](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P146_I1.png)

Two M3X6 screws

Fastener Fastener

```metadata
pagina: 146
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P146_I2.png
contexto: 
```

![Imagen página 146 - 2](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P146_I2.png)

Insert and connect recorder cable.

```metadata
pagina: 146
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P146_I3.png
contexto: 
```

![Imagen página 146 - 3](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P146_I3.png)

Air filter

Short-circuited hose

```metadata
pagina: 146
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P146_I4.png
contexto: 
```

![Imagen página 146 - 4](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P146_I4.png)

Three M2.5X4 screws

Cover

```metadata
pagina: 146
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P146_I5.png
contexto: 
```

![Imagen página 146 - 5](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P146_I5.png)

Take the silicone case out.

# Página 147

**Equipo:** Monitor multiparametrico ePM

7-66

7.5.7 Disassembling Main Bracket Component

1. Loosen the battery cover.

2. Loosen the five ST3.3X8 screws shown in the figure, and remove the main bracket component.

Note 1. Before reassembling the main bracket component, insert the connection belt of the battery cover

to the locating post of the rear housing shown in the following figure.

Note 2. Before closing the battery cover, switch the battery to the vertical position shown in the figure.

```metadata
pagina: 147
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P147_I0.png
contexto: 
```

![Imagen página 147 - 0](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P147_I0.png)

```metadata
pagina: 147
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P147_I1.png
contexto: 
```

![Imagen página 147 - 1](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P147_I1.png)

Put the battery cover aside, without closing it.

Amplified

Insert the connection belt to the locating post of the rear housing.

```metadata
pagina: 147
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P147_I2.png
contexto: 
```

![Imagen página 147 - 2](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P147_I2.png)

```metadata
pagina: 147
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P147_I3.png
contexto: 
```

![Imagen página 147 - 3](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P147_I3.png)

Open the battery cover.

Five ST3.3X8 screws

# Página 148

**Equipo:** Monitor multiparametrico ePM

7-67

7.5.8 Disassembling Speaker

1. Loosen the two ST3.3X8 screws of the speaker component shown in the figure, and take the speaker

component out.

7.5.9 Disassembling Rear Alarm Indicator (Configured)

1. Loosen the six ST3.3X8 screws on the cover component shown in the figure, and take the top cover

component out.

2. Loosen the one ST3.3X8 screw on the rear alarm indicator shown in the figure, and take the rear alarm

indicator component out.

7.5.10 Disassembling Power Module

1. Remove the AC input cable, and remove the cable connecting the power module with mainboard

out.

2. Loosen the four M3X6 screws of the power module, and take the power module out.

```metadata
pagina: 148
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P148_I0.png
contexto: 
```

![Imagen página 148 - 0](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P148_I0.png)

Two ST3.3X8 screws

```metadata
pagina: 148
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P148_I1.png
contexto: 
```

![Imagen página 148 - 1](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P148_I1.png)

```metadata
pagina: 148
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P148_I2.png
contexto: 
```

![Imagen página 148 - 2](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P148_I2.png)

After the battery is switched to the vertical position, close the battery cover.

# Página 149

**Equipo:** Monitor multiparametrico ePM

7-68

7.5.11 Disassembling SpO 2  Module (When Nellcor/Massimo SpO 2  Is Configured)

1. When Nellcor SpO 2  is configured:

Loosen the one M2X4 screw on the Nellcor SpO 2 , and take the Nellcor SpO 2  board out.

2. When Massimo SpO 2  is configured:

Loosen the two M2X4 screws on the Massimo SpO 2 , and take the Massimo SpO 2  board and insulation

sheet out.

```metadata
pagina: 149
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P149_I0.png
contexto: 
```

![Imagen página 149 - 0](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P149_I0.png)

Assemble Massimo SpO 2  board.

Use two M3X6 screws.

```metadata
pagina: 149
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P149_I1.png
contexto: 
```

![Imagen página 149 - 1](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P149_I1.png)

SpO2 board insulation sheet

```metadata
pagina: 149
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P149_I2.png
contexto: 
```

![Imagen página 149 - 2](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P149_I2.png)

One M2X4 screw

Assemble Nellcor SpO 2  board.

```metadata
pagina: 149
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P149_I3.png
contexto: 
```

![Imagen página 149 - 3](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P149_I3.png)

AC input cable

Cable connecting the mainboards

```metadata
pagina: 149
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P149_I4.png
contexto: 
```

![Imagen página 149 - 4](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P149_I4.png)

Four M3X6 screws

# Página 150

**Equipo:** Monitor multiparametrico ePM

7-69

7.5.12 Disassembling C.O. Board (Configured)

1. Remove the cable connecting the C.O. board with the mainboard.

2. Loosen the two M3X6 screws on the Massimo SpO 2 , and take the C.O. board and insulation sheet out.

7.5.13 Disassembling Mainboard

1. Remove the pump/valve connection cables from the mainboard.

2. Take the two interfaces of the NIBP hose from the mainboard sensor.

3. Remove the connection cable of the battery adapter from the mainboard.

```metadata
pagina: 150
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P150_I0.png
contexto: 
```

![Imagen página 150 - 0](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P150_I0.png)

Gas pump connection cable Gas valve connection cable

Two interfaces connecting the NIBP hose and mainboard sensor

```metadata
pagina: 150
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P150_I1.png
contexto: 
```

![Imagen página 150 - 1](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P150_I1.png)

C.O. board Black insulation sheet

Three M3X6 screws

Connection cable

# Página 151

**Equipo:** Monitor multiparametrico ePM

7-70

4. Loosen the six M3X6 screws from the main bracket in the figure.

5. Loosen the two screws on the rear of the main bracket sheet metal, and take the mainboard out.

6. As shown in the following figure, loosen the nuts or screws on the rear of the mainboard, and take

the studs out.

```metadata
pagina: 151
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P151_I0.png
contexto: 
```

![Imagen página 151 - 0](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P151_I0.png)

```metadata
pagina: 151
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P151_I1.png
contexto: 
```

![Imagen página 151 - 1](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P151_I1.png)

When the C.O. function is selected, there are three M3 nuts here.

When the Masimo SpO2 is selected, there are two M3 nuts here.

When the Nellcor SpO2 is selected, there is one M2 nut here.

When the C.O. function is selected, there are three studs here.

When the Masimo SpO2 is selected, there are two studs here.

When the Nellcor SpO2 is selected, there is one stud here.

```metadata
pagina: 151
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P151_I2.png
contexto: 
```

![Imagen página 151 - 2](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P151_I2.png)

Two screws

```metadata
pagina: 151
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P151_I3.png
contexto: 
```

![Imagen página 151 - 3](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P151_I3.png)

Six M3X6 screws

```metadata
pagina: 151
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P151_I4.png
contexto: 
```

![Imagen página 151 - 4](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P151_I4.png)

Two connection cables of the battery adapter

# Página 152

**Equipo:** Monitor multiparametrico ePM

7-71

7.5.14 Disassembling Power Adapter and NIBP Pump/Valve

1. As shown in the following figure, loosen the two ST3.3X8 screws, and take the battery adapter out.

2. Loosen the hose connecting the NIBP pump/valve.

3. Loosen the fastener fixing the NIBP valve, and take the NIBP valve out.

4. Loosen the two binding straps fixing the NIBP pump, and take the NIBP pump out.

Note: During reassembly, ensure that the hose is correctly connected with the quick/slow release valve.

```metadata
pagina: 152
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P152_I0.png
contexto: 
```

![Imagen página 152 - 0](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P152_I0.png)

Two binding straps

Loosen the fastener fixing the NIBP valve.

Loose the hose connecting the pump with the valve.

```metadata
pagina: 152
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P152_I1.png
contexto: 
```

![Imagen página 152 - 1](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P152_I1.png)

# Página 153

**Equipo:** Monitor multiparametrico ePM

7-72

7.6 ePM T10 Vehicle-mounted Charger Base Disassembly

7.6.1 Disassembling Transfer Base

1. Push the release handle towards the arrow direction marked on the handle, and take the adapter

component out upward.

```metadata
pagina: 153
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P153_I0.png
contexto: 
```

![Imagen página 153 - 0](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P153_I0.png)

```metadata
pagina: 153
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P153_I1.png
contexto: 
```

![Imagen página 153 - 1](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P153_I1.png)

2. Loosen the four M4X12 combination screws using the Phillips screwdriver, and separate the transfer

base from the installation base.

```metadata
pagina: 153
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P153_I2.png
contexto: 
```

![Imagen página 153 - 2](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P153_I2.png)

```metadata
pagina: 153
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P153_I3.png
contexto: 
```

![Imagen página 153 - 3](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P153_I3.png)

```metadata
pagina: 153
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P153_I4.png
contexto: 
```

![Imagen página 153 - 4](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P153_I4.png)

3. Use tweezers to peel the waterproof tape off. In case of reinstallation, use a new waterproof tape.

```metadata
pagina: 153
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P153_I5.png
contexto: 
```

![Imagen página 153 - 5](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P153_I5.png)

Slow release valve of blue cable

The end of the hose with a black current limiter is connected to the slow release valve the blue cable.

Four M4X12 combination screw

Transfer base Installation base

# Página 154

**Equipo:** Monitor multiparametrico ePM

7-73

```metadata
pagina: 154
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P154_I0.png
contexto: 
```

![Imagen página 154 - 0](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P154_I0.png)

```metadata
pagina: 154
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P154_I1.png
contexto: 
```

![Imagen página 154 - 1](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P154_I1.png)

4. Remove the output cable from the PCBA base, and take the cable out. Remove the input cable

terminal from the PCBA, loosen the four M3X8 screws, and take the power input connector out from

the base.

```metadata
pagina: 154
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P154_I2.png
contexto: 
```

![Imagen página 154 - 2](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P154_I2.png)

```metadata
pagina: 154
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P154_I3.png
contexto: 
```

![Imagen página 154 - 3](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P154_I3.png)

5. Loose the six M3X6 screws using a Phillips screwdriver, remove the socket of the LED indicator from

the PCBA, and take the PCBA out.

```metadata
pagina: 154
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P154_I4.png
contexto: 
```

![Imagen página 154 - 4](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P154_I4.png)

6. Use tweezers to take the conductive rubber of the PCBA from the cooling block, and pull the LED

indicator out from the base hole.

Four M3X8 screws

Six M3X6 screws

Waterproof tape

# Página 155

**Equipo:** Monitor multiparametrico ePM

7-74

```metadata
pagina: 155
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P155_I0.png
contexto: 
```

![Imagen página 155 - 0](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P155_I0.png)

```metadata
pagina: 155
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P155_I1.png
contexto: 
```

![Imagen página 155 - 1](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P155_I1.png)

7.6.2 Disassembling Installation Base

1. Use tweezers to peel the sealing tape off, and loosen the three M3X6 pan head screws with pad using

the screwdriver.

```metadata
pagina: 155
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P155_I2.png
contexto: 
```

![Imagen página 155 - 2](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P155_I2.png)

```metadata
pagina: 155
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P155_I3.png
contexto: 
```

![Imagen página 155 - 3](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P155_I3.png)

2. Take the release board and release handle out upward, loosen the two M3X6 countersunk screws

using the screwdriver, and separate the release board from the release handle.

```metadata
pagina: 155
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P155_I4.png
contexto: 
```

![Imagen página 155 - 4](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P155_I4.png)

3. Take the two locating springs out, and use the tweezers to remove the two pads.

```metadata
pagina: 155
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P155_I5.png
contexto: 
```

![Imagen página 155 - 5](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P155_I5.png)

```metadata
pagina: 155
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P155_I6.png
contexto: 
```

![Imagen página 155 - 6](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P155_I6.png)

4. Loosen the twelve M3X6 countersunk screws using the screwdriver, and remove the four locking

block press boards.

Conducti ve rubber

Three M3X6 screws

Two M3X6 countersunk screws

Release handle

Release board

Locating spring

Pad

# Página 156

**Equipo:** Monitor multiparametrico ePM

7-75

```metadata
pagina: 156
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P156_I0.png
contexto: 
```

![Imagen página 156 - 0](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P156_I0.png)

```metadata
pagina: 156
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P156_I1.png
contexto: 
```

![Imagen página 156 - 1](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P156_I1.png)

5. Take the four pressing springs and slide blocks out upward.

```metadata
pagina: 156
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P156_I2.png
contexto: 
```

![Imagen página 156 - 2](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P156_I2.png)

```metadata
pagina: 156
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P156_I3.png
contexto: 
```

![Imagen página 156 - 3](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P156_I3.png)

7.6.3 Disassembling Adapter Component

Use tweezers to take the four foot pads out from the adapter component, and loosen the four M4X10

screws using the screwdriver, and separate the installation block from the adapter.

```metadata
pagina: 156
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P156_I4.png
contexto: 
```

![Imagen página 156 - 4](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P156_I4.png)

```metadata
pagina: 156
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P156_I5.png
contexto: 
```

![Imagen página 156 - 5](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P156_I5.png)

Foot pad

Installation block

Four locking block press boards

Twelve M3X6 countersunk screws

Pressing spring

Slide block

# Página 157

**Equipo:** Monitor multiparametrico ePM

8-1

8 Parts

This part lists the exploded view and PN of the monitor, auxiliary plugin box and parameter module, so

that maintenance personnel can recognize the names of different parts when they disassemble or replace

the parts.

8.1 ePM 15/ePM 15A/ePM 15C Parts

8.1.1 System Structure

Exploded View

```metadata
pagina: 157
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P157_I0.png
contexto: 
```

![Imagen página 157 - 0](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P157_I0.png)

Parts List

No. Name and Specification Quantity PN

1 Front Housing Assembly 1 115-060001-00

2

Repair kit for integrated 15-inch rear housing component

(rear alarm light is not supported)

1 115-059949-00

Repair kit for integrated 15-inch rear housing component

(rear alarm light is supported)

1 115-059950-00

# Página 158

**Equipo:** Monitor multiparametrico ePM

8-2

8.1.2 Front Housing

Exploded View

```metadata
pagina: 158
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P158_I0.png
contexto: 
```

![Imagen página 158 - 0](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P158_I0.png)

Parts List

No. Name and Specification Quantity PN

1 TFT displayer assembly (AUO 15-inch screen) 1 115-059826-00

2 Repair kit for front housing and touch screen 1 115-060001-00

3 9202 C15 function keypad PCBA 1 115-059768-00

# Página 159

**Equipo:** Monitor multiparametrico ePM

8-3

8.1.3 Rear Housing

Exploded View

```metadata
pagina: 159
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P159_I0.png
contexto: 
```

![Imagen página 159 - 0](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P159_I0.png)

Parts List

No. Name and Specification Quantity PN

1 TR6F recorder 1 115-059807-00

2 Integrated 15-inch standard configuration mainboard FRU

(with software)

1 115-059942-00

Integrated 15-inch full configuration 3/5-lead MR SpO 2

mainboard FRU (with software)

1 115-059943-00

Integrated 15-inch full configuration 3/5-lead OEM SpO 2

mainboard FRU (with software)

1 115-059944-00

Integrated 15-inch full configuration 12-lead MR SpO 2

mainboard FRU (with software)

1 115-059945-00

Integrated 15-inch full configuration 12-lead OEM SpO 2

mainboard FRU (with software)

1 115-059946-00

3 Mindray sidestream CO 2  module kit 1 115-059955-00

4 Speaker 2W40hm 500Hz 1 115-059960-00

5 Repair kit for integrated panel component (CO 2  is not supported) 1 115-059951-00

Repair kit for integrated panel component (CO 2  is supported) 1 115-059952-00

# Página 160

**Equipo:** Monitor multiparametrico ePM

8-4

8.2 ePM 12/ePM 12A/ePM 12C Parts

8.2.1 System Structure

Exploded View

```metadata
pagina: 160
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P160_I0.png
contexto: 
```

![Imagen página 160 - 0](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P160_I0.png)

Parts List

No. Name and Specification Quantity PN

1 Front Housing Assembly 1 115-059976-00

2

Repair kit for integrated 12-inch rear housing component

(rear alarm light is not supported)

1 115-059972-00

Repair kit for integrated 12-inch rear housing component

(rear alarm light is supported)

1 115-059973-00

# Página 161

**Equipo:** Monitor multiparametrico ePM

8-5

8.2.2 Front Housing

Exploded View

```metadata
pagina: 161
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P161_I0.png
contexto: 
```

![Imagen página 161 - 0](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P161_I0.png)

Parts List

No. Name and Specification Quantity PN

1 Front Housing repair kit 1 115-059976-00

2 TFT display assembly (Innolux 12-inch screen) 1 115-059827-00

# Página 162

**Equipo:** Monitor multiparametrico ePM

8-6

8.2.3 Rear Housing

Exploded View

```metadata
pagina: 162
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P162_I0.png
contexto: 
```

![Imagen página 162 - 0](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P162_I0.png)

Parts List

No. Name and Specification Quantity PN

1

Repair kit for integrated panel component (CO 2  is not

supported)

115-059951-00

Repair kit for integrated panel component (CO 2  is supported) 115-059952-00

2 CO 2  module (M02D) 1 115-059974-00

3 Integrated 12-inch standard configuration mainboard FRU

(with software)

1

115-059965-00

Integrated 12-inch full configuration 3/5-lead MR SpO 2

mainboard FRU (with software)

1

115-059966-00

Integrated 12-inch full configuration 3/5-lead OEM SpO 2

mainboard FRU (with software)

1

115-059967-00

Integrated 12-inch full configuration 12-lead MR SpO 2

mainboard FRU (with software)

1

115-059968-00

Integrated 12-inch full configuration 12-lead OEM SpO 2

mainboard FRU (with software)

1

115-059969-00

4 Speaker repair kit 1 115-059830-00

5 TR6F recorder 1 115-059807-00

6 9202 rear alarm indicator PCBA 1 115-059941-00

# Página 163

**Equipo:** Monitor multiparametrico ePM

8-7

8.3 ePM 10/ePM 10A/ePM 10C Parts

8.3.1 System Structure

Exploded View

```metadata
pagina: 163
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P163_I0.png
contexto: 
```

![Imagen página 163 - 0](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P163_I0.png)

Parts List

No. Name and Specification Quantity PN

1

Repair kit for front housing and touch screen

(DC-in is not supported)

1 115-059997-00

Repair kit for front housing and touch screen

(DC-in is supported)

1 115-059998-00

2

Repair kit for integrated 10-inch rear housing

component (rear alarm light is not supported)

1 115-059993-00

Repair kit for integrated 10-inch rear housing

component (rear alarm light is supported)

1 115-059994-00

# Página 164

**Equipo:** Monitor multiparametrico ePM

8-8

8.3.2 Front Housing

Exploded View

```metadata
pagina: 164
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P164_I0.png
contexto: 
```

![Imagen página 164 - 0](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P164_I0.png)

Parts List

No. Name and Specification Quantity PN

1 Repair kit for front housing and touch screen 1 115-059997-00

2 TFT display assembly (Innolux 10-inch screen) 1 115-059828-00

# Página 165

**Equipo:** Monitor multiparametrico ePM

8-9

8.3.3 Rear Housing

Exploded View

```metadata
pagina: 165
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P165_I0.png
contexto: 
```

![Imagen página 165 - 0](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P165_I0.png)

Parts List

No. Name and Specification Quantity PN

1

Repair kit for front alarm light board (light

sensor is not supported)

1 115-059746-00

Repair kit for front alarm light board (light

sensor is supported)

1 115-059747-00

2 ePM battery cover connection belt 1 043-010075-00

3 TR6F recorder 1 115-059807-00

4 Speaker 1 115-059830-00

5 CO 2  module (M02D) 1 115-059974-00

6 Integrated 10-inch standard configuration

mainboard FRU (with software)

1

115-059985-00

Integrated 10-inch full configuration 3/5-lead

MR SpO 2  mainboard FRU (with software, DC-in

is not supported)

1

115-059986-00

Integrated 10-inch full configuration 3/5-lead

OEM SpO 2  mainboard FRU (with software,

DC-in is not supported)

1

115-059987-00

# Página 166

**Equipo:** Monitor multiparametrico ePM

8-10

No. Name and Specification Quantity PN

Integrated 10-inch full configuration 3/5-lead

MR SpO 2  mainboard FRU (with software, DC-in

is supported)

1

115-059988-00

Integrated 10-inch full configuration 3/5-lead

OEM SpO 2  mainboard FRU (with software,

DC-in is supported)

1

115-059989-00

# Página 167

**Equipo:** Monitor multiparametrico ePM

A-1

A Electrical Safety Inspection

The following electrical safety tests are recommended as part of a comprehensive preventive maintenance

program. They are a proven means of detecting abnormalities that, if undetected, could prove dangerous

to either the patient or the operator. Additional tests may be required according to local regulations.

All tests can be performed using commercially available safety analyzer test equipment. These procedures

assume the use of a 601PROXL International Safety Analyzer or equivalent safety analyzer. Other popular

testers complying with IEC 60601-1 used in Europe such as Fluke, Metron, or Gerb may require

modifications to the procedure. Follow the instructions of the analyzer manufacturer.

The consistent use of a safety analyzer as a routine step in closing a repair or upgrade is emphasized as a

mandatory step if an approved agency status is to be maintained. The safety analyzer also proves to be an

excellent troubleshooting tool to detect abnormalities of line voltage and grounding, as well as total

current loads.

A.1 Power Cord Plug

A.1.1 The Power Plug

Test Item Acceptance Criteria

The power plug

The power plug pins No broken or bent pin. No discolored pins.

The plug body No physical damage to the plug body.

The strain relief

No physical damage to the strain relief. No plug

warmth for device in use.

The power plug No loose connections.

The power cord

No physical damage to the cord. No deterioration to

the cord.

For devices with detachable power cords, inspect the

connection at the device.

For devices with non-detachable power cords, inspect

the strain relief at the device.

# Página 168

**Equipo:** Monitor multiparametrico ePM

A-2

A.2 Device Enclosure and Accessories

A.2.1 Visual Inspection

Test Item Acceptance Criteria

The enclosure and accessories

No physical damage to the enclosure and accessories.

No physical damage to meters, switches, connectors,

etc.

No residue of fluid spillage (e.g., water, coffee,

chemicals, etc.).

No loose or missing parts (e.g., knobs, dials, terminals,

etc.).

A.2.2 Contextual Inspection

Test Item Acceptance Criteria

The enclosure and accessories

No unusual noises (e.g., a rattle inside the case).

No unusual smells (e.g., burning or smoky smells,

particularly from ventilation holes).

No taped notes that may suggest device deficiencies

or operator concerns.

A.3 Device Labeling

Check the labels provided by the manufacturer or the healthcare facility are present and legible.

 Main unit label

 Integrated warning labels

A.4 Protective Earth Resistance

Protective Earth Resistance is measured using the RED test lead attached to the DUT Protective Earth

terminal or enclosure. Select the test current by pressing SOFT KEY 3 to toggle between 1AMP, 10AMP, and

25AMP. The front panel outlet power is turned off for this test.

# Página 169

**Equipo:** Monitor multiparametrico ePM

A-3

The following conditions apply: L1 and L2 Open.

Preparation

1. First select the test current that will be used for performing the Protective Earth Resistance test by

pressing AMPERES (SOFT KEY 3).

2. Connect the test lead(s) between the RED input jack and the GREEN input jack.

3. Press CAL LEADS. The 601PRO will measure the lead resistance, and if less than 0.150 Ohms, it will

store the reading and subtract it from all earth resistance readings taken at the calibrated current.

```metadata
pagina: 169
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P169_I0.png
contexto: 
```

![Imagen página 169 - 0](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P169_I0.png)

If the calibration fails, the previously stored readings will be used until a passing calibration has occurred.:

WARNING

 During Earth Resistance testing, the DUT must be plugged into the 601PRO front outlet. If

the DUT fails Earth Resistance, discontinue tests and label the device defective.

To Perform the Test

1. From the MAIN MENU, or with the outlet unpowered, plug the DUT into the 601PRO front panel

outlet.

2. Attach the 601PRO RED input lead to the device’s Protective Earth terminal or an exposed metal area.

3. Press shortcut key 3. The Protective Earth Resistance test is displayed.

4. Press SOFT KEY 3 to select a test current (1AMP, 10AMP, or 25AMP). The selected test current is

displayed in the upper right corner of the display.

```metadata
pagina: 169
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P169_I2.png
contexto: 
```

![Imagen página 169 - 2](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P169_I2.png)

5. Press START TEST to start the test. The test current is applied while resistance and current readings are

taken. This takes approximately 5 seconds.

6. Press the print data key at any time to generate a printout of the latest measurement(s).

# Página 170

**Equipo:** Monitor multiparametrico ePM

A-4

NOTE

 When "Over" is displayed for Ohms, this signifies that a valid measurement was not

obtained because either an open connection was detected or that the measurement was not

within range. Readings greater than 9.999 Ohms will be displayed as Over.

In Case of Failure

Once it reaches the limitation, stop using and inform the Customer Service Engineer for analysis and

disposal.

LIMITS

ALL COUNTRIES R = 0.2 Ω Maximum

A.5 Earth Leakage Test

Run an Earth Leakage test on the device being tested before performing any other leakage tests.

Leakage current is measured the following ways:

 Earth Leakage Current, leakage current measured through DUT outlet Earth

 Earth Leakage Current AP-EARTH (ALL Applied Parts connected to Earth), leakage current measured

through DUT outlet Earth

There is no need to attach a test lead; the 601PRO automatically connects the measuring device internally.

To Perform the Test

1. From the MAIN MENU, or with the outlet unpowered, plug the DUT into the 601PRO front panel

outlet, and turn on the device.

2. Attach the device's applied parts to the 601PRO applied part terminals if applicable.

3. Press shortcut key 4.The Earth Leakage test appears on the display, and the test begins immediately:

```metadata
pagina: 170
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P170_I0.png
contexto: 
```

![Imagen página 170 - 0](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P170_I0.png)

 SOFT KEY 1 toggles the DUT outlet Polarity from Normal to Off to Reverse.

# Página 171

**Equipo:** Monitor multiparametrico ePM

A-5

 SOFT KEY 2 toggles the DUT outlet from Earth to No Earth.

 SOFT KEY 3 toggles the DUT outlet from L2 to No L2.

 SOFT KEY 4 toggles the AP to Earth to No AP to Earth.

4. Press the print data key at any time to generate a printout of the latest measurement.

In Case of Failure

 Check any broken of the enclosure. Replace any defective part.

 Inspect wiring for bad crimps, poor connections, or damage.

 Test the wall outlet; verify it is grounded and is free of other wiring abnormalities. Notify the user or

owner to correct any deviations. As a work around, check the other outlets to see if they could be

used instead.

 Change another probe to confirm if the fail is caused by console.

 If the leakage current measurement tests fail on a new unit and if situation can not be corrected,

submit a Safety Failure Report to document the system problem. Remove unit from operation.

 If all else fails, stop using and inform the Customer Service Engineer for analysis and disposal.

LIMITS

For IEC60601-1,

 5mA in Normal Condition

 10mA in Single Fault Condition

A.6 Patient Leakage Current

Patient leakage currents are measured between a selected applied part and mains earth. All

measurements have a true RMS only response.

Preparation

Perform a calibration from the Mains on Applied Part menu.

The following outlet conditions apply when performing this test:

 Normal Polarity, Earth Open, Outlet ON Normal Polarity, Outlet ON

 Normal Polarity, L2 Open, Outlet ON Reversed Polarity, Outlet ON

 Reversed Polarity, Earth Open, Outlet ON Reversed Polarity, L2 Open, Outlet ON

# Página 172

**Equipo:** Monitor multiparametrico ePM

A-6

WARNING

 If all of the applied parts correspond to the instrument type, the applied parts will be tied

together and one reading will be taken. If any of the applied parts differ from the

instrument type, all applied parts will be tested individually, based on the type of applied

part. This applies to Auto and Step modes only.

To Perform the Test

1. From the MAIN MENU, or with the outlet unpowered, plug the DUT into the 601PRO front panel

outlet, and turn on the device.

2. Attach the applied parts to the 601PRO's applied part terminals.

3. Press shortcut key 6. The Patient Leakage test is displayed, and the test begins immediately.

```metadata
pagina: 172
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P172_I1.png
contexto: 
```

![Imagen página 172 - 1](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P172_I1.png)

4. Press APPLIED PART (SOFT KEY 4) at any time to select the desired applied part leakage current.

5. Modify the configuration of the front panel outlet by pressing the appropriate SOFT KEY on the

601PRO.

6. Press the print data key at any time to generate a printout of the latest measurement.

In Case of Failure

 Check any broken of the enclosure. Replace any defective part.

 Inspect wiring for bad crimps, poor connections, or damage.

 Test the wall outlet; verify it is grounded and is free of other wiring abnormalities. Notify the user or

owner to correct any deviations. As a work around, check the other outlets to see if they could be

used instead.

 Change another probe to confirm if the fail is caused by console.

 If the leakage current measurement tests fail on a new unit and if situation can not be corrected,

submit a Safety Failure Report to document the system problem. Remove unit from operation.

 If all else fails, stop using and inform the Customer Service Engineer for analysis and disposal.

# Página 173

**Equipo:** Monitor multiparametrico ePM

A-7

LIMITS

For CF

applied parts

 10μA in Normal Condition

 50μA in Single Fault Condition

For BF

applied parts

 100μA in Normal Condition

 500μA in Single Fault Condition

A.7 Mains on Applied Part Leakage

The Mains on Applied Part test applies a test voltage, which is 110% of the mains voltage, through a

limiting resistance, to selected applied part terminals. Current measurements are then taken between the

selected applied part and earth.  Measurements are taken with the test voltage (110% of mains) to

applied parts in the normal and reverse polarity conditions as indicated on the display.

The following outlet conditions apply when performing the Mains on Applied Part test.

 Normal Polarity;

 Reversed Polarity

Preparation

To perform a calibration from the Mains on Applied Part test, press CAL (SOFT KEY 2).

1. Disconnect ALL patient leads, test leads, and DUT outlet connections.

2. Press CAL to begin calibration, as shown:

```metadata
pagina: 173
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P173_I2.png
contexto: 
```

![Imagen página 173 - 2](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P173_I2.png)

If the calibration fails, the previously stored readings will be used until a passing calibration has

occurred. Also, the esc/stop key has no effect during calibration.

3. When the calibration is finished, the Mains on Applied Part test will reappear.

# Página 174

**Equipo:** Monitor multiparametrico ePM

A-8

WARNING

 A 2-beep-per-second signal indicates high voltage present at the applied part terminals

while a calibration is being performed.

 High voltage is present at applied part terminals while measurements are being taken.

To Perform the Test

1. From the MAIN MENU, or with the outlet unpowered, plug the DUT into the 601

2. Attach the applied parts to the 601PRO applied part terminals.

3. Attach the red terminal lead to a conductive part on the DUT enclosure.

4. Press shortcut key 7. The Mains on Applied Part test is displayed.

```metadata
pagina: 174
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P174_I1.png
contexto: 
```

![Imagen página 174 - 1](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P174_I1.png)

5. Select the desired outlet configuration and applied part to test using the appropriate SOFT KEYS:

6. Press START TEST (SOFT KEY 1) to begin the test.

7. Press the print data key to generate a printout of the latest measurement.

NOTE

 If all of the applied parts correspond to the instrument type, the applied parts will be tied

together and one reading will be taken. If any of the applied parts differ from the

instrument type, all applied parts will be tested individually, based on the type of applied

part. This applies to Auto and Step modes only.

In Case of Failure

 Check any broken of the enclosure. Replace any defective part.

 Inspect wiring for bad crimps, poor connections, or damage.

 Test the wall outlet; verify it is grounded and is free of other wiring abnormalities. Notify the user or

owner to correct any deviations. As a work around, check the other outlets to see if they could be

used instead.

 Change another probe to confirm if the fail is caused by console.

 If the leakage current measurement tests fail on a new unit and if situation can not be corrected,

submit a Safety Failure Report to document the system problem. Remove unit from operation.

 If all else fails, stop using and inform the Customer Service Engineer for analysis and disposal.

# Página 175

**Equipo:** Monitor multiparametrico ePM

A-9

LIMITS

 For CF

applied parts: 50 μA

 For BF

applied parts: 5000 μA

A.8 Patient Auxiliary Current

Patient Auxiliary currents are measured between any selected ECG jack and the remaining selected ECG

jacks. All measurements may have a true RMS only response.

Preparation

1. From the MAIN MENU, or with the outlet unpowered, plug the DUT into the 601PRO front panel

outlet, and turn on the device.

2. Attach the patient leads to the 601PRO ECG jacks.

3. Define the Lead Types from the View Settings Option (refer to: Lead Type Definitions in Section 5 of

this chapter).

4. Press shortcut key 8. The Patient Auxiliary Current test is displayed, and the test begins immediately.

Display values are continuously updated until another test is selected.

```metadata
pagina: 175
imagen: data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P175_I2.png
contexto: 
```

![Imagen página 175 - 2](data/images/monitor_multiparametrico_epm_series_compact_monitor_service_manual_v1_0_en/P175_I2.png)

5. Press SOFT KEYS 1-4 to select leakage tests

6. Press APPLIED PART (SOFT KEY 4) at any time to select the desired applied part leakage current:

7. Modify the configuration of the front panel outlet by pressing the appropriate SOFT KEY on the

601PRO:

8. Press the print data key at any time to generate a printout of the latest measurement.

In Case of Failure

 Check any broken of the enclosure. Replace any defective part.

 Inspect wiring for bad crimps, poor connections, or damage.

# Página 176

**Equipo:** Monitor multiparametrico ePM

A-10

 Test the wall outlet; verify it is grounded and is free of other wiring abnormalities. Notify the user or

owner to correct any deviations. As a work around, check the other outlets to see if they could be

used instead.

 Change another probe to confirm if the fail is caused by console.

 If the leakage current measurement tests fail on a new unit and if situation can not be corrected,

submit a Safety Failure Report to document the system problem. Remove unit from operation.

 If all else fails, stop using and inform the Customer Service Engineer for analysis and disposal.

LIMITS

For CF

applied parts,

 10μA in Normal Condition

 50μA in Single Fault Condition

For BF

applied parts,

 100μA in Normal Condition

 500μA in Single Fault Condition

# Página 177

**Equipo:** Monitor multiparametrico ePM

A-11

ELECTRICAL SAFETY INSPECTION FORM

Overall assessment:

Scheduled inspection Test item: 1, 2, 3, 4, 5, 6, 7, 8

Location: Technician:

Equipment: Control Number:

Manufacturer: Model: SN:

Measurement equipment /SN: Date of Calibration:

INSPECTION AND TESTING Pass/Fail Limit

1 Power Cord Plug

2 Device Enclosure and Accessories

3 Device Labeling

4 Protective Earth Resistance Ω Max 0.2 Ω

5 Earth Leakage

Normal

condition(NC)

____μA

Max:

NC: 5mA

SFC: 10mA Single Fault

condition(SFC)

____μA

6

Patient Leakage

Current

Normal

condition(NC)

□ BF____μA

Max:

CF applied part:

NC:10μA, SFC: 50μA

BF applied part:

NC:100μA, SFC: 500μA

□ CF____μA

Single Fault

condition(SFC)

□ BF____μA

□ CF____μA

7 Mains on Applied Part Leakage

□ BF____μA

Max:

CF applied part: 50μA

BF applied part: 5000μA □ CF____μA

8

Patient

Auxiliary

Current

Normal condition(NC)

□ BF____μA

Max:

CF applied part:

NC:10μA, SFC: 50μA

BF applied part:

NC:100μA, SFC: 500μA

□ CF____μA

Single Fault

condition(SFC)

□ BF____μA

□ CF____μA

Name/ Signature: __________________________ Date:_____________________________

# Página 178

**Equipo:** Monitor multiparametrico ePM

A-12

Unopened repair type Test item: 1, 2, 3

Opened repair type, not replace the power part including

transformer or patient circuit board

Test item: 1, 2, 3, 4

Opened repair type, replace the power part including transformer Test item: 1, 2, 3, 4, 5

Opened repair type, replace patient circuit board Test item: 1, 2, 3, 4, 6, 7, 8

Location: Technician:

Equipment: Control Number:

Manufacturer: Model: SN:

Measurement equipment /SN: Date of Calibration:

INSPECTION AND TESTING Pass/Fail Limit

1 Power Cord Plug

2 Device Enclosure and Accessories

3 Device Labeling

4 Protective Earth Resistance Ω Max 0.2 Ω

5 Earth Leakage

Normal

condition(NC)

____μA

Max:

NC: 5mA

SFC: 10mA Single Fault

condition(SFC)

____μA

6

Patient Leakage

Current

Normal

condition(NC)

□ BF____μA

Max:

CF applied part:

NC:10μA, SFC: 50μA

BF applied part:

NC:100μA, SFC: 500μA

□ CF____μA

Single Fault

condition(SFC)

□ BF____μA

□ CF____μA

7 Mains on Applied Part Leakage

□ BF____μA

Max:

CF applied part: 50μA

BF applied part:

5000μA

□ CF____μA

8

Patient

Auxiliary

Current

Normal condition(NC)

□ BF____μA

Max:

CF applied part:

NC:10μA, SFC: 50μA

BF applied part:

NC:100μA, SFC: 500μA

□ CF____μA

Single Fault

condition(SFC)

□ BF____μA

□ CF____μA

Name/ Signature: __________________________ Date:_____________________________

