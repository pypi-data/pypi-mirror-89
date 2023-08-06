# iragnsep

iragnsep performs IR (i.e. 8--1000 microns) SED fits, separated into AGN and galaxy contributions, and measure host galaxy properties (e.g. SFRs) free of AGN contamination. The advantage of iragnsep is that, in addition to fitting observed broadband photometric fluxes, it also allows to incorporate IR spectra in the fits which, if available, improves the robustness of the galaxy-AGN separation. 

For the galaxy component iragnsep uses a library of galaxy templates built and presented in Bernhard et al. (in prep.). In terms of the AGN contribution, if the input dataset is a mixture of spectral and photometric data, iragnsep uses a combination of power-laws for the AGN continuum, and some broad features for the silicate emission. If, instead, the dataset contains photometric data alone, the AGN contribution is accounted for by using the library of AGN templates presented in Bernhard et al. (in prep.).

The advanced fitting techniques used by iragnsep (i.e. MLE optimised with MCMC) combined with the powerful model comparison tests (i.e. AIC) allow iragnsep to provide a statistically robust interpretation of IR SEDs in terms of AGN–galaxy contributions, even when the AGN contribution is highly diluted by the host galaxy emission.

The aim of this README is to show how to use iragnsep. This document also contains important information such as limitations and cautions.

For a detailed description on the templates and fitting technique, see Bernhard et al. (in prep.).

Contacts: e.p.bernhard[at]sheffield.ac.uk

## Getting Started
These instructions should assist you in getting iragnsep running on your machine. iragnsep is written for python 3 and is available on PyPI.

### Prerequisites
iragnsep requires some non-standard libraries (dependencies) to run. These should automatically get installed when downloading and installing iragnsep via PyPi. If not, these can be manually installed using the pip3 command. The dependencies are as follow,

* [NumPy](https://numpy.org) - NumPy is the fundamental package for scientific computing with Python.
* [Matplotlib](https://matplotlib.org) - Matplotlib is a Python 2D plotting library.
* [Astropy](https://www.astropy.org) - The Astropy Project is a community effort to develop a common core package for Astronomy in Python and foster an ecosystem of inter-operable astronomy packages.
* [SciPy](https://www.scipy.org) - SciPy is a Python-based ecosystem of open-source software for mathematics, science, and engineering.
* [pandas](https://pandas.pydata.org) - pandas is an open source, BSD-licensed library providing high-performance, easy-to-use data structures and data analysis tools for the Python programming language.
* [emcee](https://emcee.readthedocs.io/en/stable/#) - emcee is an MIT licensed pure-Python implementation of Goodman & Weare’s Affine Invariant Markov chain Monte Carlo (MCMC) Ensemble sampler.
* [Numba](http://numba.pydata.org) - Numba translates Python functions to optimised machine code at runtime using the industry-standard LLVM compiler library. Numba-compiled numerical algorithms in Python can approach the speeds of C or FORTRAN.

### Installation
We recommend to install iragnsep and its dependencies using pip,

```
pip3 install iragnsep
```
The project is also publicly available on GitHub at https://tinyurl.com/y9phjhxy .

## Quick start

In this section we show how to infer the SFR of the galaxy IC5063 using iragnsep.

### Step 1: Get the data and the script

You can download the data at https://tinyurl.com/y9phjhxy. The file IC5063_photo.csv contains the photometric fluxes, and the file IC5063_IRS.csv contains the calibrated Spitzer-IRS spectrum. The file main.py is the main script. Once downloaded, create a folder with all of these files.

### Step 2: Run the script

In a terminal simply cd to the folder that contains the files and run,

```
python3 main.py
```

iragnsep is now fitting the SED, first using a combination of the IRS spectrum and Herschel photometry, then using photometry only, as if the IRS spectrum was not available. The user can open the file main.py which is commented and can be used as a template for future use of iragnsep.

### Step 3: Output

Once the fits are performed the plots and tables are generated and saved in the same folder. 

* **IC5063_fitRes_spec.csv** - contains the results of the fits for the 14 possible combinations of models considered by iragnsep. Each row corresponds to a specific model. This file contains the results of the fits performed on data which included the IRS spectrum. The best model is flagged by a value of 1.0 in the column 'bestModelFlag'. See section ** Description of the tables** for a full description.
* **IC5063_fitResAll_spec.pdf** - shows each of the 14 possible models fit to the data which included the IRS spectrum.
* **IC5063_fitResBM_spec.pdf** - shows the best fit to the data which included the IRS spectrum. The best fit corresponds to a statistically weighted sum of all of the 14 different models.
* **IC5063_fitRes_photo.csv** - contains the results of the fits for the 21 possible combinations of templates. Each row corresponds to a specific model. This file contains the results of the fits performed in photometry only (i.e. the IRS spectrum was replaced by photometry). The best model is flagged by a value of 1.0 in the column 'bestModelFlag'. See the section ** Description of the tables** for a full description.
* **IC5063_fitResAll_photo.pdf** - shows each of the 21 models fit to the photometric data.
* **IC5063_fitResBM_photo.pdf** - shows the best fit to the photometric data. The best fit corresponds to a statistically weighted sum of all of the 21 different models.

## Preparing your data
As this is the first public release of iragnsep it is important to make sure that the input data are compatible with the code. Future versions will allow more flexibility in the format of the input data. The main input are the wavelengths of the SED (or combined spectrum and photometry) and the corresponding fluxes and their uncertainties. Here is a (non-exhaustive) check list of points that are required to ensure a robust behaviour of iragnsep.

* the wavelengths are in microns, the fluxes and the uncertainties are in Jy.
* the vector wavelength is in monotonically increasing order.
* their is no negative or undefined (e.g. nan) values in the fluxes and their uncertainties (upper-limits can be passed via the keywords ULphot).
* if using iragnsep with a combination of a spectrum and photometry, make sure that no photometric points are overlapping with the spectral data (e.g. IRS spectra and MIPS 24 micron would be overlapping).
* a good value for Nmc (the number of steps in the MCMC) which esnure convergence is at least 50000 steps when the spectrum is included, and 10000 if used with photometric data only.
* do not forget to set the redshift of the source using the keyword z.
* for the photometric version, avoid photometry below roughly 5 microns rest-frame as iragnsep has not been designed to account for emissions below this value (e.g. old stellar population).

Should you find anything non-intuitive missing from the above list, contact us at: e.p.bernhard[at]sheffield.ac.uk

## Description of the tables

The output of the fits can be saved using the keyword saveRes as shown in the main.py of the Quick Start example. In particular two types of tables can be generated whether using the version of the code with spectra or that of with photometry alone.

The table sourceName_fitRes_spec.csv (where sourceName is the name of the source passed by the user) is a comma separated value (CSV) table which contains the results of the fits performed on data which included spectra. Each table row corresponds to one of the 14 possible models considered by iragnsep. Columns are as follow,

* **tplName** - the name of the galaxy template [gal1_dust, gal2_dust, gal3_dust, gal4_dust, gal5_dust, gal6_dust, gal7_dust].
* **AGNon** - if  0.0, the results are for a fit that did not contain any AGN contributions, while if 1.0, the results are for a fit that accounted for AGN contributions.
* **logNormGal_dust, elogNormGal_dust** - the log-normalisation of the galaxy dust continuum template and its uncertainties.
* **logNormGal_PAH, elognNormGal_PAH** - the log-normalisation of the PAH emission template and its uncertainties.
* **logNormAGN_PL, elogNormAGN_PL** - the overall normalisation of the continuum emission for AGN (combination of broken power-laws) and its uncertainties.
* **lBreak_PL, elBreak_PL** - the position of the main break for the AGN emission and its uncertainties.
* **alpha1, ealpha1** - the slope of the AGN power-law below 11 micron and its uncertainties.
* **alpha2, ealpha2** - the slope of the AGN power-law above 11 micron and below 18 micron and its uncertainties.
* **alpha3, ealpha3** - the slope of the AGN power-law above 18 micron and below lbreak_PL and its uncertainties.
* **logNorm_Si, elogNorm_Si** - the log-normalisation of the silicate emission.
* **dSi, edSi** - the shift of the silicate emission peak and its uncertainties.
* **loglumIR_host, eloglumIR_host** - the IR (8--1000 microns) luminosity of the host free of AGN contamination, and its uncertainties.
* **loglumMIR_host, eloglumMIR_host** - the MIR (5--35 microns) luminosity of the host free of AGN contamination, and its uncertainties.
* **loglumFIR_host, eloglumFIR_host** - the FIR (40--1000 microns) luminosity of the host free of AGN contamination, and its uncertainties.
* **loglumIR_AGN, eloglumIR_AGN** - the IR luminosity of the AGN free of host contamination, and its uncertainties.
* **loglumMIR_AGN, eloglumMIR_AGN** - the MIR luminosity of the AGN free of host contamination, and its uncertainties.
* **loglumFIR_AGN, eloglumFIR_AGN** - the FIR luminosity of the AGN free of host contamination, and its uncertainties.
* **AGNfrac_IR** - the fraction of the total IR luminosity which is attributed to the AGN, and its uncertainties.
* **AGNfrac_MIR** - the fraction of the total MIR luminosity which is attributed to the AGN, and its uncertainties.
* **AGNfrac_FIR** - the fraction of the total FIR luminosity which is attributed to the AGN, and its uncertainties.
* **SFR, eSFR** - the star formation rate free of AGN contamination, and its uncertainties.
* **wSFR, ewSFR** - the weighted star formation rate free of AGN contamination, and its uncertainties.
* **logl** - the loglikelihood of the fit given the model.
* **Aw** - the Akaike weight of the model.
* **S9p7** - the total extinction at 9.7 micron.
* **bestModelFlag** - a value of 1.0 indicates the best model.

The table sourceName_fitRes_photo.csv is a CSV table which contains the results of the fits performed on data with photometry alone. Each table row corresponds to one of the 21 possible models considered by iragnsep. Columns are as follow,

* **tplName_gal** - the name of the galaxy template [gal1_dust, gal2_dust, gal3_dust, gal4_dust, gal5_dust, gal6_dust, gal7_dust].
* **AGNon** - if  0.0, the results are for a fit that did not contain any AGN contributions, while if 1.0 the results are for a fit that accounted for AGN contributions.
* **tplName_AGN** - the name of the AGN continuum template [AGN_A, AGN_B].
* **logNormGal_dust, elogNormGal_dust** - the log-normalisation of the galaxy dust continuum template and its uncertainties.
* **logNormGal_PAH, elogNormGal_PAH** - the log-normalisation of the PAH emission template and its uncertainties.
* **logNormAGN, elogNormAGN** - the log-normalisation of the AGN continuum template and its uncertainties.
* **logNormSiem, elogNormSiem** - the log-normalisation of the silicate emission template (if included in the fit) and its uncertainties.
* **loglumIR_host, eloglumIR_host** - the IR (8--1000 microns) luminosity of the host free of AGN contamination, and its uncertainties.
* **loglumMIR_host, eloglumMIR_host** - the MIR (5--35 microns) luminosity of the host free of AGN contamination, and its uncertainties.
* **loglumFIR_host, eloglumFIR_host** - the FIR (40--1000 microns) luminosity of the host free of AGN contamination, and its uncertainties.
* **loglumIR_AGN, eloglumIR_AGN** - the IR luminosity of the AGN free of host contamination, and its uncertainties.
* **loglumMIR_AGN, eloglumMIR_AGN** - the MIR luminosity of the AGN free of host contamination, and its uncertainties.
* **loglumFIR_AGN, eloglumFIR_AGN** - the FIR luminosity of the AGN free of host contamination, and its uncertainties.
* **AGNfrac_IR** - the fraction of the total IR luminosity which is attributed to the AGN, and its uncertainties.
* **AGNfrac_MIR** - the fraction of the total MIR luminosity which is attributed to the AGN, and its uncertainties.
* **AGNfrac_FIR** - the fraction of the total FIR luminosity which is attributed to the AGN, and its uncertainties.
* **SFR, eSFR** - the star formation rate free of AGN contamination, and its uncertainties.
* **wSFR, ewSFR** - the weighted star formation rate free of AGN contamination, and its uncertainties.
* **logl** - the loglikelihood of the fit given the model.
* **Aw** - the Akaike weight of the model.
* **S9p7** - the total extinction at 9.7 micron.
* **bestModelFlag** - a value of 1.0 indicates the best model.

## The templates

irasgnsep uses a library of templates for the galaxy and the AGN emission. Interested reader are referred to Bernhard et al. (in prep.) for a detailed description of the templates. The templates are available as a CSV table at:  https://tinyurl.com/yawp96qc. Columns are as follow,

* **lambda_mic** - the wavelength in micron spanning 1--1000 microns.
* **gal1_dust, egal1_dust** - the nuLnu of the first semi-empirical galaxy continuum template, normalised to Lir (i.e. integrated from 1-1000microns), and its uncertainties.
* **gal2_dust, egal2_dust** - the nuLnu of the second semi-empirical galaxy continuum template, normalised to Lir, and its uncertainties.
* **gal3_dust, egal3_dust** -  the nuLnu of the third semi-empirical galaxy continuum template, normalised to Lir, and its uncertainties.
* **gal4_dust, egal4_dust** -  the nuLnu of the fourth semi-empirical galaxy continuum template, normalised to Lir, and its uncertainties.
* **gal5_dust, egal5_dust** -  the nuLnu of the fith semi-empirical galaxy continuum template, normalised to Lir, and its uncertainties.
* **gal6_dust, egal6_dust** -  the nuLnu of the sixth semi-empirical galaxy continuum template, normalised to Lir, and its uncertainties.
* **gal7_dust, egal7_dust** -  the nuLnu of the seventh semi-empirical galaxy continuum template, normalised to Lir, and its uncertainties.
* **gal_PAH, egal_PAH** -  the nuLnu of the PAH emission template, normalised to Lir, and its uncertainties.
* **AGN_Siem, eAGN_Siem_up, eAGN_Siem_down** -  the nuLnu of the silicate emission template, normalised to Lir, and its upper and lower uncertainties.
* **AGN_A, eAGN_A_up, eAGN_A_down** -  the nuLnu of the first AGN continuum template, normalised to Lir, and its upper and lower uncertainties.
* **AGN_B, eAGN_B_up, eAGN_B_dowm** - the nuLnu of the second AGN continuum template, normalised to Lir, and its upper and lower uncertainties.

### Filters available in iragnsep

The available filters are as follow:

* **IRAC1** - Spitzer IRAC, 3.6 micron, http://svo2.cab.inta-csic.es/theory/fps/index.php?mode=browse&gname=Spitzer
* **IRAC2** - Spitzer IRAC, 4.5 micron, http://svo2.cab.inta-csic.es/theory/fps/index.php?mode=browse&gname=Spitzer
* **IRAC3** - Spitzer IRAC, 5.8 micron, http://svo2.cab.inta-csic.es/theory/fps/index.php?mode=browse&gname=Spitzer
* **IRAC4** - Spitzer IRAC, 8.0 micron, http://svo2.cab.inta-csic.es/theory/fps/index.php?mode=browse&gname=Spitzer
* **WISE_W1** - WISE, 3.4 micron, http://svo2.cab.inta-csic.es/theory/fps/index.php?mode=browse&gname=WISE
* **WISE_W2** - WISE, 4.6 micron, http://svo2.cab.inta-csic.es/theory/fps/index.php?mode=browse&gname=WISE
* **WISE_W3** - WISE, 12 micron, http://svo2.cab.inta-csic.es/theory/fps/index.php?mode=browse&gname=WISE
* **WISE_W4** - WISE, 22 micron, http://svo2.cab.inta-csic.es/theory/fps/index.php?mode=browse&gname=WISE
* **IRAS12** - IRAS, 12 micron, http://svo2.cab.inta-csic.es/theory/fps/index.php?mode=browse&gname=IRAS
* **IRAS60** - IRAS, 60 micron, http://svo2.cab.inta-csic.es/theory/fps/index.php?mode=browse&gname=IRAS
* **IRAS100** - IRAS, 100 micron, http://svo2.cab.inta-csic.es/theory/fps/index.php?mode=browse&gname=IRAS
* **MIPS24** - Spitzer MIPS, 24 micron, http://svo2.cab.inta-csic.es/theory/fps/index.php?mode=browse&gname=Spitzer&gname2=MIPS
* **MIPS70** - Spitzer MIPS, 70 micron, http://svo2.cab.inta-csic.es/theory/fps/index.php?mode=browse&gname=Spitzer&gname2=MIPS
* **MIPS160** - Spitzer MIPS, 160 micron, http://svo2.cab.inta-csic.es/theory/fps/index.php?mode=browse&gname=Spitzer&gname2=MIPS
* **PACS70** - Herschel PACS, 70 micron, http://svo2.cab.inta-csic.es/theory/fps/index.php?mode=browse&gname=Herschel
* **PACS100** - Herschel PACS, 100 micron, http://svo2.cab.inta-csic.es/theory/fps/index.php?mode=browse&gname=Herschel
* **PACS160** - Herschel PACS, 160 micron, http://svo2.cab.inta-csic.es/theory/fps/index.php?mode=browse&gname=Herschel
* **SPIRE250ps** - Herschel SPIRE, 250 micron, http://svo2.cab.inta-csic.es/theory/fps/index.php?mode=browse&gname=Herschel&gname2=SPIRE
* **SPIRE350ps** - Herschel SPIRE, 350 micron, http://svo2.cab.inta-csic.es/theory/fps/index.php?mode=browse&gname=Herschel&gname2=SPIRE
* **SPIRE500ps** - Herschel SPIRE, 500 micron, http://svo2.cab.inta-csic.es/theory/fps/index.php?mode=browse&gname=Herschel&gname2=SPIRE

Note: to add filters please contact us at: e.p.bernhard[at]sheffield.ac.uk.

-- --

## Cautionary notes

As this is the first public release of iragnsep we suggest the user to carefully check the results, and to report anything that is possibly a bug. To do this, please contact us at: e.p.bernhard[at]sheffield.ac.uk.

The templates and models built for iragnsep are based on observations out to z~0.3. We have tested these on photometry of galaxies in the COSMOS field at higher redshifts, and the results appear to be reliable. However, there is no formal proof, and we suggest that the user carefully check results for these sources.

The templates have been derived on low-to-high luminosity AGNs 41.6 erg/s<Log10(Lx2-10kev)<45.2 erg/s. As a consequence, using iragnsep for, let's say, bright QSOs is at the User's own risks. We stress however that our AGN templates are in agreement with AGN templates for quasars.

## Future work

Future version will allow more flexible inputs for the observed data. In addition it will be possible for the user to choose a complete different set of templates, if necessary.

The model for the AGN always improve from one version to another. Please check this page for update.

So far we have tested iragnsep using data from the IRS spectra and the Herschel photometry. We plan to test the possibility to incorporate other spectral data such as future JWST data.

## Versioning

We use three numbers for the versions defined as x.y.z. If only y and z are changed the output of iragnsep is unchanged and minor patches are applied. If x changes it means that major changes have been applied, and results are likely to differ from the x-1 version. We strongly advice to specify which version of iragnsep has been used for future reference. 

The first official released version starts at x=7.

## Authors

* **Emmanuel Bernhard** - *Main author + dev. of iragnsep*
* James Mullaney
* Clive Tadhunter
* Liam Grimmett
* David Rosario
* David Alexander

The associated paper can be found at https://tinyurl.com/ydhcxxxe.

## Citation

Please cite Bernhard et al. (in prep) when using iragnsep.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details