# PEL (Perceptual Error Logarithm)
An efficient and effective full-reference perceptual analytical method, namely Perceptual Error Logarithm (PEL), to measure the image quality in consistent with subjective evaluations.

- Perceptual Error Logarithm (PEL) Method (Index) - Version 1.0 
- Copyright(c) 2024 Sergio Augusto Coelho Bezerra
- All Rights Reserved.
- e-mails: sergio.bezerra@ifam.edu.br or scoelhobezerra@gmail.com
- Data: September/2024, Manaus, Amazonas, Brazil.

The author is with Institute of Computing of the Federal University of Amazonas (ICOMP/UFAM), Federal University of Technology - Paraná (CPGEI/UTFPR), and Federal Institute of Education, Science and
Technology of Amazonas (IFAM).

Permission is granted free of charge to use, modify, or copy this software and its documentation for educational and research purposes only. This program code may not be used, rewritten or adapted as part of a 
commercial product, either software or hardware, without first obtaining permission from the authors. The authors provide no representation as to the suitability of this code for any purpose.

This is an implementation of the full-reference method for calculating the perceptual quality assessment index between two images. Please refer
to the following paper:
   Sergio A. C. Bezerra, Sergio A. C. Bezerra Júnior, José L. de S. Pio, and Keiko V. O. Fonseca. "Perceptual Error Logarithm: an efficient and effective analytical method for full-reference image quality assessment" 
submitted to IEEE Access, Sep. 2024. 

If you find any errors or would like to make any suggestions, then please send them to the email sergio.bezerra@ifam.edu.br (or scoelhobezerra@gmail.com)

How to use PEL method?
Input : (1) refImg: reference image
        (2) testImg: test image
 
Output: (1) score: output index. PEL value range [0,5], where the smaller value indicates high quality.

Example with images of the LIVE dataset.
- refImg = imread('parrots.bmp'); 
- testImg = imread('img233.bmp');
- score = PEL(refImg, testImg); 
