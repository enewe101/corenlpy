import time
from hashlib import sha1
import json
import sys
import os
import subprocess
import shutil
from multiprocessing import Process


# Constants
CORENLP_PATH = os.path.expanduser('~/corenlp')
OUTPUT_FORMAT = 'xml' # or 'text' or 'serialized'
BATCH_SIZE = 50
NER_MODEL_PROPERTIES = {
	'ner.model': (
		'edu/stanford/nlp/models/ner/'
		'english.conll.4class.distsim.crf.ser.gz'
	)
}


# Read the corenlp path from the corenlpyrc config file
try:
	CORENLP_PATH = json.loads(
		open(os.path.expanduser('~/.corenlpyrc')).read()
	)['corenlp_path']
	#print 'corenlp path is %s' % CORENLP_PATH

# Fail if the corenlpyrc file has invalid json
except ValueError:
	print 'corenlpyrc file has invalid json'
	sys.exit(1)

# Tolerate missing file or unspecified corenlp_path silently
except IOError:
	print 'no corenlpyrc file, defaulting to %s.' % CORENLP_PATH
	pass
except KeyError:
	print 'no corenlp_path specified, defaulting to %s.' % CORENLP_PATH
	pass


def corenlp(
	in_dirs=[],
	in_files=[],
	out_dir='.',
	threads=1,
	output_format='xml',
	annotators=[
		'tokenize', 'ssplit', 'pos', 'lemma', 'ner', 'parse', 'dcoref'
	],
	properties={}
):

	# Tolerate single files and single directories
	if isinstance(in_dirs, basestring):
		in_dirs = [in_dirs]
	if isinstance(in_files, basestring):
		in_files = [in_files]

	# Threads gets its own argument for convenience, but will be overridden
	# by the properties dictionary if threads is specified there too.
	properties_dict = {
		'threads': threads, 
		'annotators':', '.join(annotators)
	}
	properties_dict.update(properties)

	# Create a temporary directory in which to store the properties files and
	# list of input files
	random_hash = sha1('%s%s' % (time.time(), os.getpid())).hexdigest()[:8]
	temp_dir = '.corenlpy-%s' % random_hash
	temp_path = os.path.join(out_dir, temp_dir)
	os.makedirs(temp_path)

	# create a properties file
	properties_path = os.path.join(temp_path, 'stanford-properties.txt')
	properties_file = open(properties_path, 'w')
	for prop in properties_dict:
		properties_file.write(
			'%s = %s\n' % (prop, str(properties_dict[prop]))
		)
	properties_file.close()

	# Absolutize file paths and collect files in directories
	in_files = [os.path.abspath(f) for f in in_files]
	for in_dir in in_dirs:
		in_files += [
			os.path.join(in_dir, f)
			for f in os.listdir(in_dir)
		]

	# Ensure that the output directory exists
	if not os.path.exists(out_dir):
		os.makedirs(out_dir)

	# Setup and dispatch the pool
	parse_articles(out_dir, in_files, output_format, temp_path)

	print 'all done!'

	# Clean up the temporary files
	# shutil.rmtree(temp_path)


def parse_articles(out_dir, input_files, output_format, temp_path):

	# Write a list of files that this process should take care of
	file_list_path = os.path.join(temp_path, 'stanford-parse-file-list.txt')
	open(file_list_path, 'w').write('\n'.join(input_files) + '\n')

	# Get the properties file path
	properties_path = os.path.join(temp_path, 'stanford-properties.txt')

	# build the typical command
	jars = ['*']
	jars = [os.path.join(CORENLP_PATH, f) for f in jars]
	jars_token = ':'.join(jars)
	print jars_token
	command = [
		'java',
		'-cp',
		jars_token, 
		'-Xmx5g', 
		'edu.stanford.nlp.pipeline.StanfordCoreNLP',
		'-props',
		properties_path,
		'-outputFormat',
		output_format,
		'-filelist',
		file_list_path,
		'-outputDirectory',
		out_dir,
	]

	# run coreNLP
	returncode = subprocess.Popen(command, stderr=subprocess.STDOUT).wait()

