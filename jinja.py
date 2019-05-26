from jinja2 import Environment, FileSystemLoader
import os
import copy

generate_directory = 'generated'
database_table_name = 'appointment'

main_file = database_table_name + '.blade.php'
table_file = database_table_name + '_table_partial.blade.php'
javascript_file = database_table_name + '.js'
edit_form_file = database_table_name + '_edit_form_partial.blade.php'
store_and_update_file = 'store_and_update.php'
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
	'appointment_updated_count': ['input', 'text'],
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
edit_form = env.get_template('edit_form.txt')
store_and_update = env.get_template('store_and_update.txt')
 
##################################
#   creating main page
##################################
database_table_structure_for_main = copy.deepcopy(database_table_structure_orig)
for column_name, values_array in database_table_structure_for_main.items():
	name_array = column_name.split('_')
	name = ' '.join(name_array).title()
	values_array.insert(0, name)
	if values_array[1] == 'select':
		name_array[-1] = 'list'
		name = '_'.join(name_array)
		values_array.insert(2, name)
		name_array[-1] = 'item'
		name = '_'.join(name_array)
		values_array.insert(3, name)
		if name_array[0] == model_name.lower():
			name_array[-1] = 'code'
		else:
			name_array[-1] = 'id'
		name = '_'.join(name_array)
		values_array.insert(4, name)
		name_array[-1] = 'name'
		name = '_'.join(name_array)
		values_array.insert(5, name)


filename = os.path.join(root, generate_directory, main_file)
with open(filename, 'w') as fh:
  fh.write(main_page.render(
  	model_name = model_name,
  	database_table_structure = database_table_structure_for_main,
  ))

##################################
#   creating table
##################################
database_table_structure_for_table = copy.deepcopy(database_table_structure_orig)
for column_name, values_array in database_table_structure_for_table.items():
	name_array = column_name.split('_')
	if name_array[0] == database_table_name:
		name_array.pop(0)
	name = ' '.join(name_array).upper()
	values_array.insert(0, name)

variable_list = database_table_name + '_list'
variable_item = database_table_name + '_item'

filename = os.path.join(root, generate_directory, table_file)
with open(filename, 'w') as fh:
  fh.write(table.render(
  	variable_item = variable_item,
  	variable_list = variable_list,
  	database_table_name = database_table_name,
  	database_table_structure = database_table_structure_for_table,
  ))

##################################
#   creating javascript file
##################################
filename = os.path.join(root, generate_directory, javascript_file)
with open(filename, 'w') as fh:
  fh.write(javascript.render(
  	database_table_name = database_table_name,
  ))

##################################
#   creating edit form
##################################
filename = os.path.join(root, generate_directory, edit_form_file)
with open(filename, 'w') as fh:
  fh.write(edit_form.render(
  	database_table_name = database_table_name,
  	database_table_structure = database_table_structure_for_main,
  ))

##################################
#   creating store and update
##################################
filename = os.path.join(root, generate_directory, store_and_update_file)
with open(filename, 'w') as fh:
  fh.write(store_and_update.render(
  	model_name = model_name,
  	database_table_name = database_table_name,
  	database_table_structure = database_table_structure_orig,
  ))