# Perceptual Error Logarithm (PEL) Method (Index) - Version 1.0.1 
# Copyright(c) 2024 Sergio Augusto Coelho Bezerra
# All Rights Reserved.
# e-mails: sergio.bezerra@ifam.edu.br or scoelhobezerra@gmail.com
# Data: September/2024, Manaus, Amazonas, Brazil.
#
# The author is with Institute of Computing of the Federal University of
# Amazonas (ICOMP/UFAM), Federal University of Technology - Paraná (Brazil)
# - (CPGEI/UTFPR), and Federal Institute of Education, Science and
# Technology of Amazonas (IFAM).
#
#----------------------------------------------------------------------
# 
# Permission is granted free of charge to use, modify, or copy this 
# software and its documentation for educational and research purposes only.
# This program code may not be used, rewritten or adapted as part of a 
# commercial product, either software or hardware, without first obtaining 
# permission from the authors. The authors provide no representation as to 
# the suitability of this code for any purpose.
#----------------------------------------------------------------------
#
# This is an implementation of the full-reference method for calculating the
# perceptual quality assessment index between two images. Please refer
# to the following paper:
#
# @ARTICLE{10965688,
# author={Bezerra, Sergio A. C. and Bezerra Júnior, Sérgio A. C. and De S. Pio, José L. and Carvalho, José R. H. and Fonseca, Keiko V. O.},
# journal={IEEE Access}, 
# title={Perceptual Error Logarithm: An Efficient and Effective Analytical Method for Full-Reference Image Quality Assessment}, 
# year={2025},
# volume={13},
# number={},
# pages={68587-68606},
# keywords={Image quality;Quality assessment;Image edge detection;Distortion;Visualization;Video recording;Electronic mail;Accuracy;Standards;Real-time systems;Full-reference;perceptual analytical method;image quality assessment;gradient magnitude;contrast sensitivity;local energy;superpixel similarity;absolute difference;local standard deviation},
# doi={10.1109/ACCESS.2025.3560918}} 
#
# If you find any errors or would like to make any suggestions, then 
# please send them to the email sergio.bezerra@ifam.edu.br (or
# scoelhobezerra@gmail.com)
#
#----------------------------------------------------------------------
import cv2
import numpy as np
from scipy.ndimage import generic_filter

def stdfilt(img, window_size=3):
    """Implementação do stdfilt do MATLAB usando SciPy."""
    return generic_filter(img, np.std, size=(window_size, window_size))

def PEL_python(refImg_path, testImg_path):
    """
    Perceptual Error Logarithm (PEL) Method - Python Version
    Adaptado para retornar valores entre 0 e 1 (1 = melhor qualidade).
    """
    
    # Upload images
    refImg_orig = cv2.imread(refImg_path).astype(np.float64)
    testImg_orig = cv2.imread(testImg_path).astype(np.float64)
    
    # DOWNSIZE
    height, width = refImg_orig.shape[:2]
    # Modified to work well with HD or higher quality images.
    resize = max(2.0, max(height, width) / 512.0 + 0.5)
    resize = round(resize, 1)
    
    new_size = (int(width / resize), int(height / resize))
    refImgR = cv2.resize(refImg_orig, new_size, interpolation=cv2.INTER_AREA)
    testImgR = cv2.resize(testImg_orig, new_size, interpolation=cv2.INTER_AREA)

    # LUMINANCE and COLORSPACE CONVERSION (YIQ-like conversion used in PEL)
    # refImgR[:,:,0] = Blue, [:,:,1] = Green, [:,:,2] = Red no OpenCV
    B_r, G_r, R_r = refImgR[:,:,0], refImgR[:,:,1], refImgR[:,:,2]
    B_t, G_t, R_t = testImgR[:,:,0], testImgR[:,:,1], testImgR[:,:,2]

    refImgI = 0.596 * R_r - 0.274 * G_r - 0.322 * B_r
    testImgI = 0.596 * R_t - 0.274 * G_t - 0.322 * B_t
    
    refImgQ = 0.211 * R_r - 0.523 * G_r + 0.312 * B_r
    testImgQ = 0.211 * R_t - 0.523 * G_t + 0.312 * B_t
    
    refLuma = (0.299 * R_r + 0.587 * G_r + 0.114 * B_r)
    testLuma = (0.299 * R_t + 0.587 * G_t + 0.114 * B_t)
 
    # LOCAL STANDARD DEVIATION
    LSDr = stdfilt(refLuma)
    LSDt = stdfilt(testLuma)

    # GRADIENT MAGNITUDE (GM) - Usando Prewitt como no original
    kernelx = np.array([[1,1,1],[0,0,0],[-1,-1,-1]])
    kernely = np.array([[-1,0,1],[-1,0,1],[-1,0,1]])
    
    GMr_x = cv2.filter2D(LSDr, -1, kernelx)
    GMr_y = cv2.filter2D(LSDr, -1, kernely)
    GMr = np.sqrt(GMr_x**2 + GMr_y**2)
    
    GMt_x = cv2.filter2D(LSDt, -1, kernelx)
    GMt_y = cv2.filter2D(LSDt, -1, kernely)
    GMt = np.sqrt(GMt_x**2 + GMt_y**2)

    # CHROMINANCE AND GRADIENT ABSOLUTE DIFERENCE (AD)
    AD_I = np.abs(refImgI - testImgI)
    AD_Q = np.abs(refImgQ - testImgQ)
    AD_L = np.abs(refLuma - testLuma) 

    # CONTRAST - MICHELSON CONTRAST (MC)
    K = 1.0
    AD_G  = np.abs(GMr - GMt)
    C_G = AD_G / (GMr + GMt + K)

    # LOCAL ENERGY (LE)
    LE = GMt / np.sqrt(GMr**2 + GMt**2 + AD_G**2 + K)
    W_LE = np.std(LE**2) 
    eW_LE = np.exp(W_LE) 

    # SIMILARITY CROMINANCIA
    T1 = 1.0
    alfa = 0.05
    beta = 0.35 
    Sm_I = (2.0 * refImgI * testImgI + T1) / (refImgI**2 + testImgI**2 + T1)
    Sm_Q = (2.0 * refImgQ * testImgQ + T1) / (refImgQ**2 + testImgQ**2 + T1)
    S_G  = (2.0 * GMr * GMt + T1) / (GMr**2 + GMt**2 + T1) 

    # NEW SUPERPIXEL SIMILARITY
    S_C = Sm_I * Sm_Q
    S_SP = (S_G**(alfa + W_LE)) * np.exp(beta * (S_C - 1.0)) 
    W_SP = np.mean(S_SP)

    # QUALITY ASSESSMENT COMPUTATION
    C1 = 2.0
    C2 = 6.0
    alphaPE = 1.0 / np.exp(C1 * W_SP * (eW_LE**2))
    betaPE = C2 * eW_LE - W_SP**2 
    
    # PE Calculation (Perceptual Error)
    term_main = (np.exp(C_G)**betaPE) * (AD_G + AD_L)
    PE = alphaPE * (stdfilt(term_main) + AD_I * AD_Q)
    
    MPE = np.mean(PE)
    original_score = np.log10(MPE + K)
    
    # ADJUST FOR ML/DL (0 to 1, where 1 is perfect)
    # Since the original score ranges from 0 to 5 (0 = best):
    final_score = 1.0 - (original_score / 5.0)
    
    # Clip to ensure it stays in the range [0, 1]
    return np.clip(final_score, 0, 1)

# Example of use:
# score = PEL_python('reference.png', 'test.png')
# print(f"Qualidade PEL (0-1): {score:.4f}")