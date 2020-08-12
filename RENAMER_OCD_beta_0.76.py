#-*- coding:utf-8 -*-
### Script By: AWACS
### Name: AWA RENAMER FOR ISOTROPIX CLARISSE IFX
### Version: beta v0.76

import ix
import os

#this is a dict for some kind of OCD function
#whatever,you can add your own suffix into this dictionary
dict_suffix_short = {
	'GeometryPolyfile' : 'geo' ,
	'TextureMapFile' : 'map' ,
	'GeometryVolumeFile' : 'vdb' ,
	'GeometryBundleAlembic' : 'abc' ,
}

def Hierarchy_lister( Current_Context , as_string , is_First_iter_level):
	Hierarchy_list = []
	for ii in range (Current_Context.get_object_count() + Current_Context.get_context_count() ):
		if Current_Context.get_item(ii).is_context() is not True:
			if as_string:
				Hierarchy_list.append( str(Current_Context.get_item (ii) ) )
			else :
				Hierarchy_list.append( Current_Context.get_item (ii) ) 
			#print (Current_Context.get_item(ii))
	#print ("get_context_count " + str(Current_Context.get_context_count() ))
	for ii in range(Current_Context.get_context_count() ):
		if as_string:
			Hierarchy_list.append( str( Current_Context.get_context(ii) ) )
		else :
			Hierarchy_list.append(  Current_Context.get_context(ii) )
			#if Current_Context.get_item(ii).is_context():
		Hierarchy_list_list = Hierarchy_lister( Current_Context.get_context(ii) , True , False )
		Hierarchy_list += Hierarchy_list_list
	if is_First_iter_level :
		Hierarchy_list = list(reversed(Hierarchy_list))
	return Hierarchy_list

#COMMAND_PART
class AWA_renamer_excuter(ix.api.EventObject):
	def Search_replace(self, sender, evtid):
		ix.begin_command_batch('Undo Search_replace')
		Selected_Hierarchy = Hierarchy_checkbox.get_value()
		oldtext = oldtext_lineEdit.get_text()
		newtext = newtext_lineEdit.get_text()
		counter = 0
		for i in range( ix.selection.get_count() ):
			selected_obj = str(ix.selection[i])

			selected_obj_name = selected_obj.split('/')

			if len(oldtext) != 0 :
				new_name = selected_obj_name[-1].replace( oldtext , newtext )

				ix.cmds.RenameItem( selected_obj , new_name )

				if str(selected_obj_name[-1]) != new_name:
					counter += 1

			if Selected_Hierarchy :
				if ix.selection[i].is_context():
					Hierarchy_list = Hierarchy_lister( ix.selection[i] , True , True )
					for iii in range(len(Hierarchy_list)):
						selected_obj_name = Hierarchy_list[iii].split('/')
						if len(oldtext) != 0 :
							new_name = selected_obj_name[-1].replace( oldtext , newtext )
							ix.cmds.RenameItem( Hierarchy_list[iii] , new_name )

							if str(selected_obj_name[-1]) != new_name:
								counter += 1

		ix.log_info ( str(counter) + " Object has been renamed" + " -- from AWA renamer" )
		ix.end_command_batch()

	def add_prefix(self, sender, evtid):
		ix.begin_command_batch('Undo Add Prefix')
		Selected_Hierarchy = Hierarchy_checkbox.get_value()
		string_Prefix = Prefix_lineEdit.get_text()
		counter = 0

		for i in range( ix.selection.get_count() ):
			selected_obj = str(ix.selection[i])
			selected_obj_name = selected_obj.split('/')

			if len(string_Prefix) != 0 :
				new_name = ( string_Prefix + str(selected_obj_name[-1]))

				ix.cmds.RenameItem( selected_obj , new_name )

				if str(selected_obj_name[-1]) != new_name:
					counter += 1

				if Selected_Hierarchy :
					if ix.selection[i].is_context():
						Hierarchy_list = Hierarchy_lister( ix.selection[i] , True , True )

						for iii in range(len(Hierarchy_list)):
							selected_obj_name = Hierarchy_list[iii].split('/')
							new_name = ( string_Prefix + str(selected_obj_name[-1]))

							ix.cmds.RenameItem( Hierarchy_list[iii] , new_name )
							if str(selected_obj_name[-1]) != new_name :
								counter += 1
		ix.log_info (str(counter) + " Object has been added your Prefix" + " -- from AWA renamer" )
		ix.end_command_batch()

	def add_suffix(self, sender, evtid):
		ix.begin_command_batch('Undo Add Suffix')
		Selected_Hierarchy = Hierarchy_checkbox.get_value()
		string_Suffix = Suffix_lineEdit.get_text()
		counter = 0

		for i in range( ix.selection.get_count() ):
			selected_obj = str(ix.selection[i])
			selected_obj_name = selected_obj.split('/')

			if len(string_Suffix) != 0 :
				new_name = ( str(selected_obj_name[-1]) + string_Suffix )

				ix.cmds.RenameItem( selected_obj , new_name )

				if str(selected_obj_name[-1]) != new_name:
					counter += 1
				if Selected_Hierarchy :
					if ix.selection[i].is_context():
						Hierarchy_list = Hierarchy_lister( ix.selection[i] , True , True )
						
						# for iii in range(len(Hierarchy_list)):
						# 	print (Hierarchy_list[iii])
						for iii in range(len(Hierarchy_list)):
							selected_obj_name = Hierarchy_list[iii].split('/')
							new_name = ( str(selected_obj_name[-1]) + string_Suffix)

							ix.cmds.RenameItem( Hierarchy_list[iii] , new_name )
							if str(selected_obj_name[-1]) != new_name :
								counter += 1

		ix.log_info (str(counter) + " Object has been added your Suffix" + " -- from AWA renamer" )
		ix.end_command_batch()

	def Filereader_Renamer(self, sender, evtid):
		ix.begin_command_batch('Undo Filereader Rename')
		Selected_Hierarchy = Hierarchy_checkbox.get_value()
		file_suffix = file_suffix_checkbox.get_value()
		object_type_suffix = object_type_suffix_checkbox.get_value()
		counter = 0
		for i in range(ix.selection.get_count() ):
			selected_obj = str(ix.selection[i])
			selected_obj_name = selected_obj.split('/')
			
			#True Type
			if ix.selection[i].is_context() is False :
				object_type_fullname = ix.selection[i].get_class_name()
				if object_type_fullname in dict_suffix_short:
					#has dirctory
					if  len( str( ix.selection[i].attrs.filename) )  > 2 :
						filename_full_path = ix.selection[i].attrs.filename
						#print (filename_full_path[0])
						file_name_and_extension = os.path.splitext( os.path.split( str(filename_full_path[0]) )[1])
						#print (file_name_and_extension)
						new_name = file_name_and_extension[0]
						if file_suffix :
							new_name = new_name + "_" + file_name_and_extension[1][ 1: ]
						if object_type_suffix :
							new_name = new_name + "_" + dict_suffix_short.get(object_type_fullname)
							
						ix.cmds.RenameItem( selected_obj , new_name )
						if str(selected_obj_name[-1]) != new_name : counter += 1

			if Selected_Hierarchy :
				if ix.selection[i].is_context():
					Hierarchy_list = Hierarchy_lister( ix.selection[i] , True , True )

					for iii in range(len(Hierarchy_list)):
						
						selected_obj_name = str(Hierarchy_list[iii]).split('/')
						
						#True Type
						if Hierarchy_list[iii].is_context() is False :
							object_type_fullname = Hierarchy_list[iii].get_class_name()
							if object_type_fullname in dict_suffix_short:
								#has dirctory
								if  len( str( Hierarchy_list[iii].attrs.filename) )  > 2 :
									filename_full_path = Hierarchy_list[iii].attrs.filename
									#print (filename_full_path[0])
									file_name_and_extension = os.path.splitext( os.path.split( str(filename_full_path[0]) )[1])
									#print (file_name_and_extension)
									new_name = file_name_and_extension[0]
									if file_suffix : new_name = new_name + "_" + file_name_and_extension[1][ 1: ]
									if object_type_suffix : new_name = new_name + "_" + dict_suffix_short.get(object_type_fullname)
										
									ix.cmds.RenameItem( Hierarchy_list[iii] , new_name )
									if str(selected_obj_name[-1]) != new_name : counter += 1

		ix.log_info (str(counter) + " Object has been renamed" + " -- from AWA renamer")
		ix.end_command_batch()

	def combiner_group_Renamer(self, sender, evtid):
		ix.begin_command_batch('Undo Combiner Group Rename')
		Selected_Hierarchy = Hierarchy_checkbox.get_value()
		object_type_suffix = combiner_group_object_type_suffix_checkbox.get_value()
		counter = 0
		for i in range(ix.selection.get_count() ):
			selected_obj = str(ix.selection[i])
			selected_obj_name = selected_obj.split('/')

			if ix.selection[i].is_context() is False :
				object_type_fullname = ix.selection[i].get_class_name()
				#True Type
				#SceneObjectCombiner
				if object_type_fullname == "SceneObjectCombiner":
					#has dirctory
					if  len(str( ix.selection[i].attrs.objects ) )  > 1 :
					
						First_Ref_Path = str(ix.selection[i].attrs.objects[0])
						new_name = First_Ref_Path.split('/')[-1]
						if object_type_suffix == 1:
							new_name = new_name + "_" + "Combiner"
							
						ix.cmds.RenameItem( selected_obj , new_name )
						if str(selected_obj_name[-1]) != new_name : counter += 1
				#True Type
				#SceneObjectCombiner
				if object_type_fullname == "Group":
					#has dirctory
					if  len(str( ix.selection[i].attrs.inclusion_items ) )  > 1 :

						First_Ref_Path = str(ix.selection[i].attrs.inclusion_items[0])
						new_name = First_Ref_Path.split('/')[-1]
						if object_type_suffix == 1:
							new_name = new_name + "_" + "Group"
							
						ix.cmds.RenameItem( selected_obj , new_name )
						if str(selected_obj_name[-1]) != new_name : counter += 1

			if Selected_Hierarchy :
				if ix.selection[i].is_context():
					Hierarchy_list = Hierarchy_lister( ix.selection[i] , True , True )
					for iii in range(len(Hierarchy_list)):
						
						selected_obj_name = str(Hierarchy_list[iii]).split('/')
						if Hierarchy_list[iii].is_context() is False :
							object_type_fullname = Hierarchy_list[iii].get_class_name()
							#True Type
							#SceneObjectCombiner
							if object_type_fullname == "SceneObjectCombiner":
								#has dirctory
								if  len(str( Hierarchy_list[iii].attrs.objects ) )  > 1 :
									First_Ref_Path = str(Hierarchy_list[iii].attrs.objects[0])
									new_name = First_Ref_Path.split('/')[-1]
									if object_type_suffix == 1:
										new_name = new_name + "_" + "Combiner"
									ix.cmds.RenameItem( Hierarchy_list[iii] , new_name )
									if str(selected_obj_name[-1]) != new_name : counter += 1
							#True Type
							#SceneObjectCombiner
							if object_type_fullname == "Group":
								if len(str( Hierarchy_list[iii].attrs.inclusion_items ) )  > 1 :
									First_Ref_Path = str(Hierarchy_list[iii].attrs.inclusion_items[0])
									new_name = First_Ref_Path.split('/')[-1]
									if object_type_suffix == 1:
										new_name = new_name + "_" + "Group"
									ix.cmds.RenameItem( Hierarchy_list[iii] , new_name )
									if str(selected_obj_name[-1]) != new_name : counter += 1

		ix.log_info ( str(counter) + " Object has been renamed" + " -- from AWA renamer" )
		ix.end_command_batch()

#GUI_PART
appwindow_x = ix.application.get_event_window().get_position()[0]
appwindow_y = ix.application.get_event_window().get_position()[1]
window_title = "Rename Tool OCD v0.76"
AWA_renamer_window = ix.api.GuiWindow(ix.application.get_event_window(), appwindow_x + 180, appwindow_y + 60, 320, 320 , window_title)
#panels
panel_0 = ix.api.GuiPanel(AWA_renamer_window, 0, 0, AWA_renamer_window.get_width(), 30)
panel_1 = ix.api.GuiPanel(AWA_renamer_window, 0, 30, AWA_renamer_window.get_width(), 100)
panel_2 = ix.api.GuiPanel(AWA_renamer_window, 0, 130, AWA_renamer_window.get_width(), 80)
panel_3 = ix.api.GuiPanel(AWA_renamer_window, 0, 210, AWA_renamer_window.get_width(), 60)
panel_4 = ix.api.GuiPanel(AWA_renamer_window, 0, 270, AWA_renamer_window.get_width(), 50)
#Hierarchy_checkbox
Hierarchy_checkbox  = ix.api.GuiCheckbox(panel_0,10,10,"Including Selected Hierarchy")
#panel_1 Search_And_Replace
oldtext_label = ix.api.GuiLabel(panel_1,10,40,100,24,"Search for :")
newtext_label = ix.api.GuiLabel(panel_1,10,70,100,24,"Replace with :")
oldtext_lineEdit = ix.api.GuiLineEdit(panel_1,90,40,200,24,"")
newtext_lineEdit = ix.api.GuiLineEdit(panel_1,90,70,200,24,"")
#selectedonly_checkbox = ix.api.GuiCheckbox(panel_1,120,80,"Selected")
Search_And_Replace_Button = ix.api.GuiPushButton(panel_1,190,100,120,25,"Search & Replace")
#panel_2 prefix suffix
Prefix_label = ix.api.GuiLabel(panel_2,10,140,80,24,"Prefix :")
Suffix_label = ix.api.GuiLabel(panel_2,10,170,80,24,"Suffix :")
Prefix_lineEdit = ix.api.GuiLineEdit(panel_2,60,140,120,24,"")
Suffix_lineEdit = ix.api.GuiLineEdit(panel_2,60,170,120,24,"")
add_prefix_Button = ix.api.GuiPushButton(panel_2,190,140,120,25,"Add Prefix")
add_suffix_Button = ix.api.GuiPushButton(panel_2,190,170,120,25,"Add Suffix")
#panel_3 Filereader combiner group referencer
file_suffix_checkbox = ix.api.GuiCheckbox(panel_3,10,220,"File Suffix")
object_type_suffix_checkbox = ix.api.GuiCheckbox(panel_3,10,245,"Object Type Suffix")
Filereader_Renamer_Button = ix.api.GuiPushButton(panel_3,150,230,160,25,"Rename Filereader Object")
#panel_4 combiner_group_Renamer
combiner_group_object_type_suffix_checkbox = ix.api.GuiCheckbox(panel_4,10,285,"Object Type Suffix")
combiner_group_Renamer_Button = ix.api.GuiPushButton(panel_4,150,280,160,25,"Rename Combiner/Group")
#connect command
events = AWA_renamer_excuter()
events.connect(Search_And_Replace_Button , 'EVT_ID_PUSH_BUTTON_CLICK', events.Search_replace)
events.connect(add_prefix_Button , 'EVT_ID_PUSH_BUTTON_CLICK', events.add_prefix)
events.connect(add_suffix_Button , 'EVT_ID_PUSH_BUTTON_CLICK', events.add_suffix)
events.connect(Filereader_Renamer_Button , 'EVT_ID_PUSH_BUTTON_CLICK', events.Filereader_Renamer)
events.connect(combiner_group_Renamer_Button , 'EVT_ID_PUSH_BUTTON_CLICK', events.combiner_group_Renamer)

AWA_renamer_window.show()
while AWA_renamer_window.is_shown(): ix.application.check_for_events()