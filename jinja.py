from jinja2 import Environment, FileSystemLoader
import os

generate_directory = 'generated'
database_table_name = 'appointment'

main_file = database_table_name + '.blade.php'
table_file = database_table_name + '_table_partial.blade.php'
javascript_file = database_table_name + '.js'
model_name = database_table_name.title()

# format => 'column_name': ['html tag', 'type:if_any']
database_table_structure_orig = {
	'appointment_title': ['input', 'text'],
	'appointment_number': ['input', 'text'],
	'appointment_comment': ['textarea'],
	'appointment_comment_internal': ['textarea'],
	'appointment_contact_first_name': ['input', 'text'],
	'appointment_contact_last_name': ['input', 'text'],
	'appointment_contact_email': ['input', 'email'],
	'appointment_contact_mobile': ['input', 'text'],
	'appointment_address_line_1': ['input', 'text'],
	'appointment_address_line_2': ['input', 'text'],
	'appointment_city': ['input', 'text'],
	'appointment_province_code': ['input', 'text'],
	'appointment_country_code': ['input', 'text'],
	'appointment_scheduled_datetime': ['input', 'text'],
	'appointment_type_code': ['select'],
	'appointment_status_code': ['select'],
	'appointment_update_count': ['input', 'text'],
	'service_id': ['select'],
	'client_id': ['select'],
	'provider_id': ['select']
}

root = os.path.dirname(os.path.abspath(__file__))
template_dir = os.path.join(root, 'templates')
os.mkdir(generate_directory)

env = Environment( loader = FileSystemLoader(template_dir), lstrip_blocks = True, trim_blocks = True )
main_page = env.get_template('main_page.txt')
table = env.get_template('table.txt')
javascript = env.get_template('javascript.txt')
 
##################################
#   creating main page
##################################
database_table_structure = database_table_structure_orig
for column_name in database_table_structure:
	name_array = column_name.split('_')
	name = ' '.join(name_array).title()
	database_table_structure[column_name].insert(0, name)
	if database_table_structure[column_name][1] == 'select':
		name_array[-1] = 'list'
		name = '_'.join(name_array)
		database_table_structure[column_name].insert(2, name)
		name_array[-1] = 'item'
		name = '_'.join(name_array)
		database_table_structure[column_name].insert(3, name)
		if name_array[0] == model_name.lower():
			name_array[-1] = 'code'
		else:
			name_array[-1] = 'id'
		name = '_'.join(name_array)
		database_table_structure[column_name].insert(4, name)
		name_array[-1] = 'name'
		name = '_'.join(name_array)
		database_table_structure[column_name].insert(5, name)


filename = os.path.join(root, generate_directory, main_file)
with open(filename, 'w') as fh:
  fh.write(main_page.render(
  	model_name = model_name,
  	database_table_structure = database_table_structure,
  ))

##################################
#   creating table
##################################
database_table_structure = database_table_structure_orig
for column_name in database_table_structure:
	name_array = column_name.split('_')
	if name_array[0] == database_table_name:
		name_array.pop(0)
	name = ' '.join(name_array).upper()
	database_table_structure[column_name].insert(0, name)

variable_list = database_table_name + '_list'
variable_item = database_table_name + '_item'

filename = os.path.join(root, generate_directory, table_file)
with open(filename, 'w') as fh:
  fh.write(table.render(
  	variable_item = variable_item,
  	variable_list = variable_list,
  	database_table_name = database_table_name,
  	database_table_structure = database_table_structure,
  ))

##################################
#   creating javascript file
##################################
filename = os.path.join(root, generate_directory, javascript_file)
with open(filename, 'w') as fh:
  fh.write(javascript.render(
  	database_table_name = database_table_name,
  ))