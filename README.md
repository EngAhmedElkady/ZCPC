# ICPC-Platform
<h1 align="center">ICPC Platform System</h1>
<h3 align="center">Let's design a ICPC Platform System</h3>

**We'll cover the following:**

* [System Requirements](#system-requirements)
* [Use Case Diagram](#use-case-diagram)
* [Class Diagram](#class-diagram)
* [Activity Diagrams](#activity-diagrams)
* [Usage](#code)

A ICPC Platform System is a software built to handle the primary main functions of a ICPC. Platform rely on communities and famous road maps . Platform systems help members to train on the open rounds for any community and help leaders to create a communities, as well as members’ subscriptions and profiles.

ICPC Platform systems also involve full automation function that help communities to follow up the levels for the members like as:
- email after each week with top member 
- remove member from round ( you will put the constrains like as who solved less than 60% from sheet will removed)
- after end week the system will write post on your page on facebook to the top 10 with photos (the community save the design only on the database)
- all member will recived email with analysis after each round 


### System Requirements

<p align="center">
    <b>
        <i>
            Always clarify requirements at the beginning of the interview. Be sure to ask questions to find the exact scope of the system that the interviewer has in mind.
        </i>
    </b>
</p>

We will focus on the following set of requirements while designing the Library Management System:

1. Any ICPC member should be able to search communities by their title, university, subject category as well by the publication date.
2. Each community will have a unique identification number and other details including a university name.
3. There are levels for each community 
4. Level consist of modules(weeks)
5. Each module have the content and sheet with problem
6. The system should be able to retrieve information like team for each community and member for each round.
7. The members can make feedback about each round and instructor and mentors.
8. The system make sort the communities by the point (from the feedback) .
9. The system should be able to collect fines for books returned after the due date.
10.The community can make the rols to join for this round you should member from this university or make it public.

### Use Case Diagram
<img src="system_design/images/">
