import nuke

# Credit + splash. A failure here must never break the menu.
try:
    import nk_credit
    nk_credit.install()
except Exception as e:
    print("nk_credit not loaded: %s" % e)


m = nuke.menu('Nuke').addMenu('NK_Tools')

############################################# Gizmos #############################################

m.addSeparator()
m.addCommand('Lens_Edge_Extend', 'nuke.createNode("Lens_Edge_Extend")')
