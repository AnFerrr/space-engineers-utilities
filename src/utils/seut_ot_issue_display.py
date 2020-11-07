import bpy
import time
import textwrap

from bpy.types              import Operator
from bpy.props              import StringProperty


class SEUT_OT_IssueDisplay(Operator):
    """Displays a list of the last 10 notifications originating from SEUT"""
    bl_idname = "wm.issue_display"
    bl_label = "SEUT Notifications"
    bl_options = {'REGISTER', 'UNDO'}


    issues_sorted = []


    def execute(self, context):

        wm = context.window_manager
        
        SEUT_OT_IssueDisplay.issues_sorted.clear()
        SEUT_OT_IssueDisplay.issues_sorted = sorted(wm.seut.issues, key=lambda issue: issue.timestamp)
        
        wm.seut.issue_alert = False
        
        return context.window_manager.invoke_popup(self, width=600)


    def draw(self, context):

        wm = context.window_manager
        layout = self.layout

        layout.label(text="SEUT Notifications", icon='INFO')

        if len(SEUT_OT_IssueDisplay.issues_sorted) < 1:
            layout.label(text="SEUT has not generated any notifications so far.")
        else:
            layout.label(text="This list displays the last 20 notifications generated by SEUT.")

        for issue in SEUT_OT_IssueDisplay.issues_sorted:
            box = layout.box()

            split = box.split(factor=0.85)

            row = split.row()
            if issue.issue_type == 'ERROR':
                row.alert = True
                row.label(text="", icon='CANCEL')
            elif issue.issue_type == 'WARNING':
                row.label(text="", icon='ERROR')
            else:
                row.label(text="", icon='INFO')
            row.label(text=issue.issue_type)
            row.label(text=issue.code)
            row.label(text=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(issue.timestamp)))

            col = box.column()
            if issue.issue_type == 'ERROR':
                col.alert = True

            wrapp = textwrap.TextWrapper(width=110)
            text_list = wrapp.wrap(text=issue.text)
            for text in text_list:
                col.label(text=text)

            row = split.row()
            if issue.issue_type == 'ERROR':
                row.alert = True
            if issue.issue_type == 'ERROR' or issue.issue_type == 'WARNING':
                semref = row.operator('wm.semref_link', text="SEMREF", icon='INFO')
                semref.section = ''
                semref.page = 'troubleshooting'
                semref.code = '#' + issue.code.lower()