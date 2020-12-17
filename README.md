# ModoBot

TODO:

- [x] `ban` command to ban a user from the server
- [x] `unban` command to revoke a ban from the server
- [x] `warn` to warn a user of his actions
- [x] `clear` to clear a count of mesages from a channel
- [x] `note` To set a note on a user, visible only by moderator
- [x] `search` Gets all info in db of passed user id (bans, notes, warnings, mutes)
- [x] `lock` locks a channel
- [x] `unlock` unlocks a channel
- [x] `info` Get info on the accounts (created, joined etc)
- [x] `mute` Mutes a user
- [x] `unmute` Unmutes a user
- [x] Pretty help page
- [x] Add action logs (log what action a moderator takes)
- [x] Finer permissions and role handling
- [x] DB for managing roles and permissions
- [x] Auto import of roles
- [x] pretty embeds for all messages
- [x] Tout mettre en français
- [x] Add a admin interface on flask
- [x] Add task to check if members that were supposed to be unmuted during server downtime be unmuted
- [x] Only resp staff and above can warn/ban moderators https://gist.github.com/OneEyedKnight/9e1b2c939185df87bb6dfff0330df9f0#file-moderation-py-L5
- [x] Cannot ban user above you
- [x] Add times in embeds in footers
- [x] Pretty embeds for locks
- [x] Add more emojis
- [x] Add check to not do anything on the bot
- [ ] Check all possible errors
- [ ] Redo error embeds.
- [ ] Dissalow double mutes/bans/etc
- [ ] When a user is muted remove all roles and put them back after
- [ ] Add reports for unauthorized use of command
- [ ] Add lots of logging
- [ ] Allow clear to be used everywhere
- [ ] Add auto unlock after a period of time
- [ ] Automatically send archive
- [ ] Flask search page

V2:

- [ ] `delnote` Deletes a note
- [ ] `delwarn` Deletes a warning
- [ ] `aban` Ask for ban (modotests)
- [ ] `aunban` Ask for unban (< resp staff)
- [ ] Move commands to COGS
- [ ] An appeal system where when a user is banned, he can appeal to ask to be redeemed for his ban
- [ ] custom commands for channels (`!salon`)
- [ ] Improve search results (Nicer look and better text)
- [ ] Add command that shows what role can do which command
- [ ] Add warning count to user, add ban after 5 warns
- [ ] Warns expire after a certain time
- [ ] Add reason for lock
- [ ] Stats for overall moderation and stats per moderator
- [ ] Relational db to link actions to moderators
