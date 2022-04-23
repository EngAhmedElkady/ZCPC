Welcome to the ICPC-Platform wiki!
# ICPC-Platform
<h1 align="center">ICPC Platform System</h1>
<h3 align="center">Let's design a ICPC Platform System</h3>

**We'll cover the following:**

* [System Requirements](#system-requirements)
* [Use Case Diagram](#use-case-diagram)
* [Class Diagram](#class-diagram)
* [Activity Diagrams](#activity-diagrams)
* [Usage](#code)

An ICPC Platform System is software built to handle the primary main functions of an ICPC. Platforms rely on communities and famous road maps. The platform system helps members to train on the open rounds for any community and helps leaders to create communities, as well as members’ subscriptions and profiles.

ICPC Platform systems also involve full automation functions that help communities to follow up the levels for the members like as:
- email after each week with the top member 
- remove a member from the round ( you will put the constraints like as who solved less than 60% from the sheet will remove)
- after the end week the system will write post on your page on Facebook to the top 10 with photos (the community saves the design only on the database)
- all member will receive email with an analysis after each round 


### System Requirements

<p align="center">
    <b>
        <i>
            Always clarify requirements at the beginning of the interview. Be sure to ask questions to find the exact scope of the system that the interviewer has in mind.
        </i>
    </b>
</p>

We will focus on the following set of requirements while designing the Library Management System:

1. Any ICPC member should be able to search communities by their title, university, and subject category as well as by the publication date.
2. Each community will have a unique identification number and other details including a university name.
3. There are levels for each community 
4. Level consists of modules(weeks)
5. Each module has the content and sheet with the problem
6. The system should be able to retrieve information like the team for each community and member for each round.
7. The members can make feedback about each round and instructor and mentors.
8. The system makes sorts the communities by the point (from the feedback).
9. The system should be able to collect fines for books returned after the due date.
10. The community can make the rolls to join for this round you should member from this university or make it public.

### Use Case Diagram
<img src="system_design/images/Use case diagram(1).png">
