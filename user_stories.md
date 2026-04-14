# User Stories:
As a Tennis Club officer, I want to build a bracket for a tennis tournament that evenly pairs opponents with players of similar skill level so that matches are fair.

As a recreational Tennis player, I want to track my first and second serve percentage so I can win more tennis matches.

As a recreational Tennis player, I want to track how many break points I get and convert so I can win my matches more consistently.

As a Tennis Club officer, I want to build a ranking system for individual players so that I can compare skill levels.

As a Tennis tournament organizer, I want to make a live tennis tournament and broadcast player stats and points during matches so that viewers can follow along.

As a Tennis Club officer, I want to be able to organize events so that players in the club can play competitive matches.

As a Tennis Club officer, I want to see the final score of a match so that future match making is better.

As a Tennis player, I want to find players of similar skill level so that I can request to play with them.

As a Tennis player, I want to look up opponents in tournaments so that I can see their previous matches and wins.

As a Tennis tournament organizer, I want to seed players in a bracket so that stronger players are placed correctly.

As a Tennis player, I want to see my past match stats so that I can track my improvement.

As a Tennis Club officer, I want to record number of sets and games won so that match results are stored correctly.
 
# Exceptions:
A player hasn't been added to the database. When the brackets are made, they aren't placed in the tournament and the officer is notified to add them first.

A player doesn't have any data on a specific stat, so when calculated it could cause a divide by zero error. The system will instead show that the stat is unavailable.

A Club officer sends out invitations to an unpublished event. A 404 error is shown when players click the invitation.

A duplicate player is added. The system will stop the entry and ask if the user wants to update the existing player instead.

There is an odd number of players in a tournament. The system will assign a bye or notify the organizer.

An invalid match score is entered. The system will reject the score and ask for a valid one.

Seeding data is missing. The system will still create the bracket but without seeding and notify the organizer.

An unauthorized user tries to edit tournament data. The system will deny access and show an error.

Live match stats fail to update. The system will show the last saved data and notify the organizer.

Internet connection is lost while entering scores. The system will warn the user that the data may not have been saved.

A player cannot find someone with similar skill level. The system will suggest the closest available match.

Not enough players join a tournament. The system will not create the bracket and notify the organizer. 


