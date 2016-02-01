import listing

loader = listing.ListingLoader()

for line in open("keywords.txt"):
    keyword = line.strip()
    keyword = '"%s"' % keyword
    loader.loadUrls(keyword)

loader.close()
