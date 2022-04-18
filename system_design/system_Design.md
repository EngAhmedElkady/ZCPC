# ICPC Platform
## business logic
- ### the user can register on the website ok, after this he can do the following.
    - See all communities.
    - Create a community.
    - join to the community if this community open trainnig 


- ### Community have levels, each level contains modules(level break into several weeks(modules)).
    - render all student
    - create form for training in some level.
    - have full automation(after end from main fauture we will do it)
    - render the team
    - 

    

---
## user:
-  ## attributes:
   - username  (uniqe) (required)
   - name      (famouse name)
   - email  (uniqe) (required)
   - codeforces_account (required)
   - github_account
   - bio
   - photo
- ## methods:
    - get_all_communities: return In all communities, this user participates in it
    - get_rate: return the rate in eatch round and the average rate

---

## community:
- ## attributes
    - name 
    - start_created
    - unversity
    - photo
- ## methods:
    - get_number_of_students: return number of all student participate in rounds for this community
    - get_team: return the team


---
## user_community:
- ## attributes
    - user-id
    - community_id
    - role  (leader - instructor - student )

- ## methods:
    - get_number_of_students: return number of all student participate in rounds for this community
    - get_team: return the team



   

