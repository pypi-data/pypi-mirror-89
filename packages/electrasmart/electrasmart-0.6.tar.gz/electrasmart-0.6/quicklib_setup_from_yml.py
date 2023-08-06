# -------- quicklib direct/bundled import, copy pasted --------------------------------------------
import sys as _sys, glob as _glob, os as _os
is_packaging = not _os.path.exists("PKG-INFO")
if is_packaging:
    import quicklib
else:
    zips = _glob.glob("quicklib_incorporated.*.zip")
    if len(zips) != 1:
        raise Exception("expected exactly one incorporated quicklib zip but found %s" % (zips,))
    _sys.path.insert(0, zips[0]); import quicklib; _sys.path.pop(0)
# -------------------------------------------------------------------------------------------------

ql_setup_kwargs = {'name': 'electrasmart', 'description': 'API client for electra air conditioner models that support the ElectraSmart app', 'top_packages': ['electrasmart'], 'version_module_paths': ['electrasmart'], 'manifest_extra': ['include electrasmart/example_status.json'], 'install_requires': ['requests'], 'entry_points': {'console_scripts': ['electrasmart-auth = electrasmart.cli:auth', 'electrasmart-list-devices = electrasmart.cli:list_devices', 'electrasmart-gen-baseline-status = electrasmart.cli:gen_baseline_status', 'electrasmart-send-command = electrasmart.cli:send_command']}, 'author': 'Yonatan Perry', 'author_email': 'yonatan.perry@gmail.com', 'license': 'This project is licensed under the terms of the MIT license', 'platforms': 'any', 'classifiers': ['Programming Language :: Python', 'Development Status :: 4 - Beta', 'Natural Language :: English', 'Operating System :: OS Independent', 'Topic :: Software Development :: Libraries :: Python Modules'], 'python_requires': '>=3.3'}    

quicklib.setup(
    **ql_setup_kwargs
)
