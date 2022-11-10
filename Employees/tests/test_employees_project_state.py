from odoo.tests.common import TransactionCase,tagged

@tagged('post_install', '-at_install')
class TestEmployeesProjectState(TransactionCase):
    
    def setUp(self, *args, **kwargs):
        super(TestEmployeesProjectState, self).setUp(*args , **kwargs)
        self.test_project = self.env['employees.project'].create({'name' : 'Project T'})
        print('a')
    def test_action_start(self):
        self.test_project.action_finish()
        self.assertEqual(self.test_project.state, 'finish' ,'Project has been finished')
        
    def test_action_close(self):
        self.test_project.action_cancel()
        self.assertEqual(self.test_project.state, 'cancel', 'Project has been canceled')