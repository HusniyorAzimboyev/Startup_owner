try:
    from apps.mentor.views import session_planner
    print('? session_planner view imported successfully')
    print(f'  Type: {type(session_planner)}')
    print(f'  Module: {session_planner.__module__}')
except ImportError as e:
    print(f'? Import Error: {e}')
except Exception as e:
    print(f'? Error: {type(e).__name__}: {e}')
