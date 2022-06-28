# This script gets ERA5 temperature data that is missing from the /badc store
#
# Uses conda environment 'ecmwf-cds', within jaspy
# Setup by:
# export PATH=/apps/contrib/jaspy/miniconda_envs/jaspy3.7/m3-4.6.14/bin:$PATH
# source activate jaspy3.7-m3-4.6.14-r20190627
# Peter Uhe
# 2020/01/21
# edited: Emily Vosper 12/08/2021
# cdo tutorial northern hemisphere https://code.mpimet.mpg.de/projects/cdo/wiki/Tutorial
# remap https://nicojourdain.github.io/students_dir/students_netcdf_cdo/
import os
import cdsapi
import subprocess
# import utils
​
outdir = '/bp1store/geog-tropical/data/ERA-5/day'
tmpdir = '/bp1store/geog-tropical/data/ERA-5/tmp'
tmpdir = '/tmp'
# if not os.path.exists(tmpdir):
#     os.mkdir(tmpdir)
print('beginning download')
# Produce ist of months 
def generate_yrmonths():
	years = range(1970,1979)
	months = ['01','02','03','04','05','06','07','08','09','10','11','12']
	yrmonths = [ int("%s%s" % (year,month)) for year in years for month in months]
	return yrmonths
​
#yrmonths = generate_yrmonths()
yrmonths = ['202203']
c = cdsapi.Client()
​
​
for yrmonth in yrmonths:
	year = str(yrmonth)[:4]
	mon  = str(yrmonth)[4:6]
​
	# Check if the files (for tas, tasmin, tasmax) are already there:
	# outfiles = glob.glob(os.path.join(outdir,'ERA5_tas*_day_'+year+mon+'.nc'))
	# if len(outfiles) == 3:
	# 	print('Files exist, skipping')
	# 	continue
​
	print('Processing:',year,mon)
​
	tmpfile =  os.path.join(tmpdir,'ERA5_tas_hrly_'+year+mon+'.nc')
​
	request = {
				'product_type': 'reanalysis',
				'format': 'netcdf',
				'variable': '2m_temperature',
				'year': year,
				'month': mon,
				'day': [
					'01', '02', '03',
					'04', '05', '06',
					'07', '08', '09',
					'10', '11', '12',
					'13', '14', '15',
					'16', '17', '18',
					'19', '20', '21',
					'22', '23', '24',
					'25', '26', '27',
					'28', '29', '30',
					'31',
				],		
				'time': [
					'00:00', '01:00', '02:00',
					'03:00', '04:00', '05:00',
					'06:00', '07:00', '08:00',
					'09:00', '10:00', '11:00',
					'12:00', '13:00', '14:00',
					'15:00', '16:00', '17:00',
					'18:00', '19:00', '20:00',
					'21:00', '22:00', '23:00',
				],}
​
	print(request)
	# c.retrieve('reanalysis-era5-single-levels-preliminary-back-extension',request,tmpfile)
	c.retrieve('reanalysis-era5-single-levels',request,tmpfile)
	print('Downloaded',tmpfile)
​
	ftas = os.path.join(outdir,'ta','tas','ERA5_tas_day_'+year+mon+'.nc')
	cdo_cmd = ['cdo','-O','-b','F32','daymean',tmpfile,ftas]
	print(' '.join(cdo_cmd))
	ret = subprocess.call(cdo_cmd)
	if not ret==0:
		raise Exception('Error with cdo command')
​
	ftasmin = os.path.join(outdir,'tasmin','ERA5_tasmin_day_'+year+mon+'.nc')
	cdo_cmd = ['cdo','-O','-b','F32','daymin',tmpfile,ftasmin]
	print(' '.join(cdo_cmd))
	ret = subprocess.call(cdo_cmd)
	if not ret==0:
		raise Exception('Error with cdo command')
​
	ftasmax = os.path.join(outdir,'tasmax','ERA5_tasmax_day_'+year+mon+'.nc')
	cdo_cmd = ['cdo','-O','-b','F32','daymax',tmpfile,ftasmax]
	print(' '.join(cdo_cmd))
	ret = subprocess.call(cdo_cmd)
	if not ret==0:
		raise Exception('Error with cdo command')
​
	os.remove(tmpfile)
	print('Finished')
​
