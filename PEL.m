function score = PEL(refImg, testImg)
% Perceptual Error Logarithm (PEL) Method (Index) - Version 1.0 
% Copyright(c) 2024 Sergio Augusto Coelho Bezerra
% All Rights Reserved.
% e-mails: sergio.bezerra@ifam.edu.br or scoelhobezerra@gmail.com
% Data: September/2024, Manaus, Amazonas, Brazil.
%
% The author is with Institute of Computing of the Federal University of
% Amazonas (ICOMP/UFAM), Federal University of Technology - Paraná (Brazil)
% - (CPGEI/UTFPR), and Federal Institute of Education, Science and
% Technology of Amazonas (IFAM).
%
%----------------------------------------------------------------------
% 
% Permission is granted free of charge to use, modify, or copy this 
% software and its documentation for educational and research purposes only.
% This program code may not be used, rewritten or adapted as part of a 
% commercial product, either software or hardware, without first obtaining 
% permission from the authors. The authors provide no representation as to 
% the suitability of this code for any purpose.
%----------------------------------------------------------------------
%
% This is an implementation of the full-reference method for calculating the
% perceptual quality assessment index between two images. Please refer
% to the following paper:
%
% Sergio A. C. Bezerra, Sergio A. C. Bezerra Júnior, José L. de S. Pio, and
% Keiko V. O. Fonseca. "Perceptual Error Logarithm: an efficient and 
% effective analytical method for full-reference image quality assessment" 
% submitted to IEEE Access, Sep. 2024. 
%
% If you find any errors or would like to make any suggestions, then 
% please send them to the email sergio.bezerra@ifam.edu.br (or
% scoelhobezerra@gmail.com)
%
%----------------------------------------------------------------------
%
% How to use PEL method?
% Input : (1) refImg: reference image
%         (2) testImg: test image
 
% Output: (1) score: output index. PEL value range [0,5], 
%                   where the smaller value indicates high quality.
%
% Example with images of the LIVE dataset.
% refImg = imread('parrots.bmp'); 
% testImg = imread('img233.bmp');
% score = PEL(refImg, testImg); 

% DOWNSIZE
resize = 2; 
refImgR = imresize(refImg, 1/(resize));
testImgR = imresize(testImg, 1/(resize));

%LUMINANCE and COLORSPACE CONVERSION 
colorImage = size(refImgR,3) == 3;  
if colorImage   
    refImgI = 0.596 * double(refImgR(:,:,1)) - 0.274 * double(refImgR(:,:,2)) - 0.322 * double(refImgR(:,:,3));
    testImgI = 0.596 * double(testImgR(:,:,1)) - 0.274 * double(testImgR(:,:,2)) - 0.322 * double(testImgR(:,:,3));
    refImgQ = 0.211 * double(refImgR(:,:,1)) - 0.523 * double(refImgR(:,:,2)) + 0.312 * double(refImgR(:,:,3));
    testImgQ = 0.211 * double(testImgR(:,:,1)) - 0.523 * double(testImgR(:,:,2)) + 0.312 * double(testImgR(:,:,3));
    refImg = (0.299* double(refImgR(:,:,1)) + 0.587* double(refImgR(:,:,2)) + 0.114  * double(refImgR(:,:,3)));
    testImg = (0.299* double(testImgR(:,:,1)) + 0.587 * double(testImgR(:,:,2)) + 0.114  * double(testImgR(:,:,3)));  
else
    refImg = (0.299* double(refImgR(:,:,1)) + 0.587* double(refImgR(:,:,2)) + 0.114  * double(refImgR(:,:,3)));
    testImg = (0.299* double(testImgR(:,:,1)) + 0.587 * double(testImgR(:,:,2)) + 0.114  * double(testImgR(:,:,3)));
end
 
% LOCAL STANDARD DEVIATION
LSDr = stdfilt(refImg);
LSDt = stdfilt(testImg);



% GRADIENT MAGNITUDE (GM)
[GMr] = imgradient(LSDr,'prewitt'); 
[GMt] = imgradient(LSDt,'prewitt'); 


% CHROMINANCE AND GRADIENT ABSOLUTE DIFERENCE (AD) OF THE CROMA
AD_I = abs(refImgI - testImgI);  
AD_Q = abs(refImgQ - testImgQ);
AD_L = abs(refImg - testImg); 

% CONTRAST - MICHELSON CONTRAST (MC)
K = 1;
AD_G  = abs(GMr - GMt);
C_G = AD_G./(GMr + GMt + K);

% LOCAL ENERGY (LE)
LE = GMt./sqrt( GMr.^2 + GMt.^2 + AD_G.^2 + K);
W_LE = std2(LE.^2); 
eW_LE = exp(W_LE); 

%SIMILARITY CROMINANCIA
T1 = 1;
alfa = 0.05; 
beta = 0.35; 
Sm_I = (2.*refImgI.*testImgI + T1)./(refImgI.^2 + testImgI.^2 + T1);  
Sm_Q = (2.*refImgQ.*testImgQ + T1)./(refImgQ.^2 + testImgQ.^2 + T1);
S_G   = (2.*GMr.*GMt + T1)./(GMr.^2 + GMt.^2 + T1); 

% NEW SUPERPIXEL SIMILARITY
S_C = Sm_I.*Sm_Q;
S_SP = (S_G.^(alfa + W_LE)).*exp(beta*( S_C - 1)); 
W_SP = mean2(S_SP);

% QUALITY ASSESSMENT COMPUTATION
alphaPE = 1/exp(2*W_SP*(eW_LE^2));
betaPE = 6.0*eW_LE - W_SP^2; 
PE = alphaPE*( stdfilt( (exp(C_G).^betaPE).*(AD_G + AD_L) ) +  AD_I.*AD_Q ) ; 
MPE = mean2(PE) ;  
K = 1;
score = log10(MPE + K) ; 
if(score== Inf || score > 5)
  score = 5;  
end 
end  

