Every branch contains programs with different purposes. They can be combined for creating a more complex analysis of the movie.
Contents:
1. Frame summarizer - version 0, has issues with sorting the frames in the chronological order
2. Frame summarizer - version 1, the issues from the previous version are fixed

3. Diarization (without statistics extracted)
4. Diarization + statistics (to be improved in the future with more information output)

5. Speeding-up movie script - for accelerating the speed of a movie (!!! the "speed" setting from the configuration file is poorly expressed as speed, it actually represent how much of the original movie we want to obtain after increasing the speed; for example: speed=0.8 => you'll obtain a video reduced to 80% of the original)
6. Movie summarizer with selective acceleration => obtain a sped up version of the original movie where less important scenes (music, noise, silence) are played much faster than the more important parts of the film (dialogue) ---> the first version is not compatible with subtitles
7. Movie summarizer with selective acceleration => the last version pushed is compatible with subtitles if the user provides an srt subtitle file

To be expected in the near future: 
Movie summarizer with selective acceleration  -> the subtitles will be synchronized for both methods (ina and srt)t
                                              -> a new method to be implemented, by combining the benefits of both current options
