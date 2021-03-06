#-*-coding:utf8-*-
#!/usr/bin/python

import unittest
import notegui
from lib.pythonmock.mock import Mock

#import wx

class NoteTaskBarTestCase(unittest.TestCase):
    def setUp(self):
        self.app = notegui.wx.App()
        self.taskbar = notegui.NoteTaskBar()
        self.menuNameSet = ['새 노트','노트 목록','환경 설정','종료']


    def test_init_taskbar(self):
        """태스크바가 제대로 생성됨"""
        self.assertTrue(isinstance(self.taskbar,notegui.NoteTaskBar))

    def test_menu_names(self):
        """태스크바 메뉴 이름들이 정상적임"""
        for item in self.taskbar.menu.GetMenuItems():
            print item.GetLabel()
#            self.assertTrue(item.GetLabel() in self.menuNameSet)


    def test_menu_new(self):
        """태스크바의 new 메뉴가 정상적으로 작동함"""
        """new 메뉴가 정상적으로 dialog를 호출하고 ID_OK까지 정상작동함"""
        menu_new = None
        for item in self.taskbar.menu.GetMenuItems():
            if item.GetLabel() == unicode("새 노트",'utf-8'):
#            if item.GetLabel() == u"새 노트":              #같은 의미
                menu_new = item
        print menu_new
        self.assertTrue(menu_new)
        event = notegui.wx.CommandEvent(notegui.wx.wxEVT_COMMAND_BUTTON_CLICKED,menu_new.GetId())
        self.taskbar.menu.GetEventHandler().ProcessEvent(event)
        print "select_note : %s" % self.taskbar.select_note
        self.assertTrue(isinstance(self.taskbar.select_note,notegui.SelectNoteDlg))

### 이벤트가 완료된 상황에서 뭔가 처리해줘야 함 


    def test_menu_list(self):
        menu_list = None
        for item in self.taskbar.menu.GetMenuItems():
            if item.GetLabel() == unicode("노트 목록",'utf-8'):
                menu_list = item
        print menu_list
        self.assertTrue(menu_list)
        event = noteguit.wx.CommandEvent(notegui.wx.wxEVT_COMMAND_BUTTON_CLICKED,menu_list.GetId())
        self.taskbar.menu.GetEventHandler().ProcessEvent(event)

    def test_menu_config(self):
        menu_config = None
        for item in self.taskbar.menu.GetMenuItems():
            if item.GetLabel() == unicode("환경 설정",'utf-8'):
                menu_config = item
        #print menu_config
        self.assertTrue(menu_config)
        class TestException(Exception): pass
        def event_callback_mock(event):
            print 'ok'
            #return True
            raise TextException
        #self.taskbar.Bind(wx.EVT_MENU, event_callback_mock, id=notegui.ID_TASK_CONFIG)

        #event = wx.CommandEvent(wx.EVT_MENU, menu_config.GetId())
#        self.taskbar.PopupMenu(self.taskbar.menu)
#        event = notegui.wx.CommandEvent(notegui.wx.wxEVT_TASKBAR_CLICK, menu_config.GetId())
#        print self.taskbar.menu.GetEventHandler().ProcessEvent(event)
        #self.assertRaises(TestException, self.taskbar.menu.GetEventHandler().ProcessEvent, event)

    def test_menu_quit(self):
        menu_quit = None
        for item in self.taskbar.menu.GetMenuItems():
            if item.GetLabel() == unicode("종료",'utf-8'):
                menu_quit = item
        print menu_quit
        self.assertTrue(menu_quit)

        class TestException(Exception): pass
        def event_callback_mock(event):
            print 'ok'
            #return True
            raise TextException
        self.taskbar.Bind(notegui.wx.EVT_MENU, event_callback_mock, id=notegui.ID_TASK_QUIT)

        event = notegui.wx.CommandEvent(notegui.wx.wxEVT_COMMAND_BUTTON_CLICKED,menu_quit.GetId())
        #print self.taskbar.menu.GetEventHandler().ProcessEvent(event)
        self.assertRaises(TestException, self.taskbar.menu.GetEventHandler().ProcessEvent, event)

class NoteGuiTestCase(unittest.TestCase):
    def setUp(self):
        self.note = None

    def test_timer(self):
        timer_event = None
        self.note.GetEventHandler().ProcessEvent(timer_event)
        pass

class NormalNoteTestCase(unittest.TestCase):
    def setUp(self):
        self.app = notegui.wx.App()
        self.body = '''
            this is real body.<br />
            and this is a text.<br />
        '''
        self.source = '''
<div id="body">%s</div>
Here is a HIDDEN header for 
<div id="page_header"><p id="is_open">True</p><p id="type">1</p></div>
SpringMemo! Don't delete this line PLEASE :)
        ''' % self.body

    def test1_parses_data_from_source_well(self):
        page_mock = Mock()
        page_mock.source = self.source
        memo_mock = Mock()
        memo_mock.page = page_mock

        normalnote = notegui.NormalNote(None,-1,"title",memo_mock)
        self.assertEqual(normalnote.body,self.body)




if __name__ == '__main__':
    loader = unittest.defaultTestLoader
    loader.testMethodPrefix = 'test1'
    unittest.main(testLoader = loader)



