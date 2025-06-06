# PEL (Perceptual Error Logarithm)
An efficient and effective full-reference perceptual analytical method, namely Perceptual Error Logarithm (PEL), to measure the image quality in consistent with subjective evaluations.

- Perceptual Error Logarithm (PEL) Method (Index) - Version 1.0.1 
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

- S. A. C. Bezerra, S. A. C. Bezerra, J. L. De S. Pio, J. R. H. Carvalho and K. V. O. Fonseca, "Perceptual Error Logarithm: An Efficient and Effective Analytical Method for Full-Reference Image Quality Assessment," in IEEE Access, vol. 13, pp. 68587-68606, 2025, doi: 10.1109/ACCESS.2025.3560918.

BibTex
- @ARTICLE{10965688,
  author={Bezerra, Sergio A. C. and Bezerra, Sérgio A. C. and De S. Pio, José L. and Carvalho, José R. H. and Fonseca, Keiko V. O.},
  journal={IEEE Access}, 
  title={Perceptual Error Logarithm: An Efficient and Effective Analytical Method for Full-Reference Image Quality Assessment}, 
  year={2025},
  volume={13},
  number={},
  pages={68587-68606},
  doi={10.1109/ACCESS.2025.3560918}}

If you find any errors or would like to make any suggestions, then please send them to the email sergio.bezerra@ifam.edu.br (or scoelhobezerra@gmail.com)

How to use PEL method?

### Input :

(1) refImg: reference image

(2) testImg: test image
 
### Output: 

(1) score: output index. PEL value range [0;5], where the smaller value indicates high quality.

Example with images of the LIVE dataset.
- refImg = imread('parrots.bmp'); 
- testImg = imread('img233.bmp');
- score = PEL(refImg, testImg); 

## Databases
- The Databases folder contains the experiment configuration files, which have 3 columns: reference images, test images, and DMOS/MOS.
