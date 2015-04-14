# Python >= 2.5 has hashlib
try:
    from hashlib import md5
    def md5_sum(s):
        return md5(s).hexdigest()
except:
    print "ERROR: No hashlib found. Using md5 instead."
    import md5
    def md5_sum(s):
        return md5.new(s).hexdigest()
