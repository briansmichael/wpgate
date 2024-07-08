Whispering Pines Gate
Administrator's Guide

Table of Contents
System Setup
Component Vendors
Command Structure
Use Cases
Troubleshooting

## Roles
There are several roles used by the gate text message system.  These roles are used to allow certain users access to system functions applicable to their role within the community.  These roles include:

* Banned - A user who has been banned from accessing the gate text message system.  Only system administrators may mark a user as being banned
* Resident - A user with limited access to the gate text messaging system.  Typically family members of homeowners within the community
* Owner - A user who is a homeowner within the community
* Admin - A user with elevated priveleges, so as to be able to maintain the system or configure the system on behalf of other users.

## Command Summary
Below is a short summary of all the possible ways to interact with the gate text message system.

### All Users
* help - Returns a brief help response to the requestor

### Guests (includes `All Users` commands)
* << house number >> << message >> - See [`Guests`](#Guests) section in this document

### Residents (includes `All Users` commands)
* open - Opens the gate

### Owners (includes `Residents` commands)
* access list - Responds to the requestor with property access configuration
* history - Responds to the requestor with property access history
* add << 10-digit phone number >> << role >> - Adds a phone number to the requestor's property configuration, assuming the phone number is not already configured in the system.  See < TBD >
* remove << 10-digit phone number >> << role >> - Removes a phone number from the requestor's property configuration.  See < TBD >

### Admins (includes `Owners` commands)
* access list all - Responds to the requestor with all properties access configuration
* history all - Responds to the requestor with all access history
* add << 10-digit phone number >> << role >> << house number >> - Adds a phone number to the requestor's property configuration, assuming the phone number is not already configured in the system.  See < TBD >
* remove << 10-digit phone number >> << role >> << house number >> - Removes a phone number from the requestor's property configuration.  See < TBD >
* ban << 10-digit phone number >> - Bans a phone number from being able to interact with the gate text messaging system
