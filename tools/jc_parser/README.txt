Johnson-Charniak Parser V1.0

Requirements
============

Requires XFVB, TkInter and ImageMagick for displaying NLTK's parse trees.

::

	sudo apt-get install python-tk -y
	sudo apt-get install imagemagick
	sudo apt-get install xvfb -y
	export DISPLAY=:1
	Xvfb :1 -screen 0 1024x768x24 &
	sudo xhost +
	sudo echo "export DISPLAY=:1" >> ~/.bashrc


Acknowledgements
================

This galaxy tool makes use of the 2015.07.23 release of the bllipparser. 
Eugene Charniak and Mark Johnson. "Coarse-to-fine n-best parsing and MaxEnt discriminative reranking." Proceedings of the 43rd Annual Meeting on Association for Computational Linguistics. Association for Computational Linguistics, 2005.

The BLLIP parser (also known as the Charniak-Johnson parser or Brown Reranking Parser) is described in the paper Charniak and Johnson (Eugene Charniak and Mark Johnson. "Coarse-to-fine n-best parsing and MaxEnt discriminative reranking." Proceedings of the 43rd Annual Meeting on Association for Computational Linguistics. Association for Computational Linguistics, 2005).
The authors request acknowledgement in any publications that make use of this software and any code derived from this software. 
Please report the release date of the software that you are using, as this will enable others to compare their results to yours.