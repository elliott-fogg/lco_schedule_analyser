# It looks like the contention of the network is to split the RA span (24 hours)
# into chunks. For each configuration of each request, add the duration of the
# configuration to the nearest bin of the RA of its target.

# For the pressure on the network, the total required time of the observing
# block is divided by the sum total time that it is seeable by all telescopes
# (i.e. the length of time visible on telescope_1 + the length of time visible
#  on  telescope_2 + ... etc). For each time bin that these windows overlap,
# this value is then divided by the number of telescopes that can see it during
# that time bin, and then added to that bin.

# https://github.com/LCOGT/observation-portal/blob/master/observation_portal/requestgroups/contention.py
