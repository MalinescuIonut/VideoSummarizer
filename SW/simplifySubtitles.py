#from textblob import TextBlob
import pysrt
import re

abbreviations = ['Dr.','Mr.','Mrs.','Ms.','etc.','Jr.','e.g.'] # You get the idea!
abbrev_replace = ['Dr','Mr','Mrs','Ms','etc','Jr','eg']
subs = pysrt.open('file.srt.old')
subs_dict = {}          # Dictionary to accumulate new sub-titles (start_time:[end_time,sentence])
start_sentence = True   # Toggle this at the start and end of sentences

# regex to remove html tags from the character count
tags = re.compile(r'<.*?>')

# regex to split on ".", "?" or "!" ONLY if it is preceded by something else
# which is not a digit and is not a space. (Not perfect but close enough)
# Note: ? and ! can be an issue in some languages (e.g. french) where both ? and !
# are traditionally preceded by a space ! rather than!
end_of_sentence = re.compile(r'([^\s\0-9][\.\?\!])')

# End of sentence characters
eos_chars = set([".","?","!"])

for sub in subs:
    if start_sentence:
        start_time = sub.start
        start_sentence = False
    text = sub.text

    #Remove multiple full-stops e.g. "and ....."
    text = re.sub('\.+', '.', text)

    # Optional
    for idx, abr in enumerate(abbreviations):
        if abr in text:
            text = text.replace(abr,abbrev_replace[idx])
    # A test could also be made for initials in names i.e. John E. Rotten - showing my age there ;)

    multi = re.split(end_of_sentence,text.strip())
    cps = sub.characters_per_second

    # Test for a sub-title with multiple sentences
    if len(multi) > 1:
        # regex end_of_sentence breaks sentence start and sentence end into 2 parts
        # we need to put them back together again.
        # hence the odd range because the joined end part is then deleted
        for cnt in range(divmod(len(multi),2)[0]): # e.g. len=3 give 0 | 5 gives 0,1  | 7 gives 0,1,2
            multi[cnt] = multi[cnt] + multi[cnt+1]
            del multi[cnt+1]

        for part in multi:
            if len(part): # Avoid blank parts
                pass
            else:
                continue
            # Convert start time to seconds
            h,m,s,milli = re.split(':|,',str(start_time))
            s_time = (3600*int(h))+(60*int(m))+int(s)+(int(milli)/1000)

            # test for existing data
            try:
                existing_data = subs_dict[str(start_time)]
                end_time = str(existing_data[0])
                h,m,s,milli = re.split(':|,',str(existing_data[0]))
                e_time = (3600*int(h))+(60*int(m))+int(s)+(int(milli)/1000)
            except:
                existing_data = []
                e_time = s_time

            # End time is the start time or existing end time + the time taken to say the current words
            # based on the calculated number of characters per second
            # use regex "tags" to remove any html tags from the character count.

            e_time = e_time + len(tags.sub('',part)) / cps

            # Convert start to a timestamp
            s,milli = divmod(s_time,1)
            m,s = divmod(int(s),60)
            h,m = divmod(m,60)
            start_time = "{:02d}:{:02d}:{:02d},{:03d}".format(h,m,s,round(milli*1000))

            # Convert end to a timestamp
            s,milli = divmod(e_time,1)
            m,s = divmod(int(s),60)
            h,m = divmod(m,60)
            end_time = "{:02d}:{:02d}:{:02d},{:03d}".format(h,m,s,round(milli*1000))

            # if text already exists add the current text to the existing text
            # if not use the current text to write/rewrite the dictionary entry
            if existing_data:
                new_text = existing_data[1] + " " + part
            else:
                new_text = part
            subs_dict[str(start_time)] = [end_time,new_text]

            # if sentence ends re-set the current start time to the end time just calculated
            if any(x in eos_chars for x in part):
                start_sentence = True
                start_time = end_time
                print ("Split",start_time,"-->",end_time,)
                print (new_text)
                print('\n')
            else:
                start_sentence = False

    else:   # This is Not a multi-part sub-title

        end_time = str(sub.end)

        # Check for an existing dictionary entry for this start time
        try:
            existing_data = subs_dict[str(start_time)]
        except:
            existing_data = []

        # if it already exists add the current text to the existing text
        # if not use the current text
        if existing_data:
            new_text = existing_data[1] + " " + text
        else:
            new_text = text
        # Create or Update the dictionary entry for this start time
        # with the updated text and the current end time
        subs_dict[str(start_time)] = [end_time,new_text]

        if any(x in eos_chars for x in text):
            start_sentence = True
            print ("Single",start_time,"-->",end_time,)
            print (new_text)
            print('\n')
        else:
            start_sentence = False

# Generate the new sub-title file from the dictionary
idx=0
outfile = open('file.srt','w')
for key, text in subs_dict.items():
    idx+=1
    outfile.write(str(idx)+"\n")
    outfile.write(key+" --> "+text[0]+"\n")
    outfile.write(text[1]+"\n\n")
outfile.close()
