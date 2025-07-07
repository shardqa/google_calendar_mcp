# TODO

- [ ] Analyse why on cursor is listing tools, but showing red. This is the logs:
2025-07-06 23:35:24.371 [info] user-google_calendar: Handling DeleteClient action
2025-07-06 23:35:24.372 [info] user-google_calendar: Cleaning up
2025-07-06 23:35:25.454 [info] user-google_calendar: Handling CreateClient action
2025-07-06 23:35:25.454 [info] user-google_calendar: Starting new stdio process with command: /home/richard_rosario/git/google_calendar_mcp/run_mcp.py
2025-07-06 23:35:25.630 [info] user-google_calendar: Successfully connected to stdio server
2025-07-06 23:35:25.630 [info] user-google_calendar: Storing stdio client
2025-07-06 23:35:25.632 [error] user-google_calendar: Client error for command [
  {
    "code": "invalid_union",
    "unionErrors": [
      {
        "issues": [
          {
            "code": "invalid_union",
            "unionErrors": [
              {
                "issues": [
                  {
                    "code": "invalid_type",
                    "expected": "string",
                    "received": "null",
                    "path": [
                      "id"
                    ],
                    "message": "Expected string, received null"
                  }
                ],
                "name": "ZodError"
              },
              {
                "issues": [
                  {
                    "code": "invalid_type",
                    "expected": "number",
                    "received": "null",
                    "path": [
                      "id"
                    ],
                    "message": "Expected number, received null"
                  }
                ],
                "name": "ZodError"
              }
            ],
            "path": [
              "id"
            ],
            "message": "Invalid input"
          },
          {
            "code": "invalid_type",
            "expected": "string",
            "received": "undefined",
            "path": [
              "method"
            ],
            "message": "Required"
          },
          {
            "code": "unrecognized_keys",
            "keys": [
              "error"
            ],
            "path": [],
            "message": "Unrecognized key(s) in object: 'error'"
          }
        ],
        "name": "ZodError"
      },
      {
        "issues": [
          {
            "code": "invalid_type",
            "expected": "string",
            "received": "undefined",
            "path": [
              "method"
            ],
            "message": "Required"
          },
          {
            "code": "unrecognized_keys",
            "keys": [
              "id",
              "error"
            ],
            "path": [],
            "message": "Unrecognized key(s) in object: 'id', 'error'"
          }
        ],
        "name": "ZodError"
      },
      {
        "issues": [
          {
            "code": "invalid_union",
            "unionErrors": [
              {
                "issues": [
                  {
                    "code": "invalid_type",
                    "expected": "string",
                    "received": "null",
                    "path": [
                      "id"
                    ],
                    "message": "Expected string, received null"
                  }
                ],
                "name": "ZodError"
              },
              {
                "issues": [
                  {
                    "code": "invalid_type",
                    "expected": "number",
                    "received": "null",
                    "path": [
                      "id"
                    ],
                    "message": "Expected number, received null"
                  }
                ],
                "name": "ZodError"
              }
            ],
            "path": [
              "id"
            ],
            "message": "Invalid input"
          },
          {
            "code": "invalid_type",
            "expected": "object",
            "received": "undefined",
            "path": [
              "result"
            ],
            "message": "Required"
          },
          {
            "code": "unrecognized_keys",
            "keys": [
              "error"
            ],
            "path": [],
            "message": "Unrecognized key(s) in object: 'error'"
          }
        ],
        "name": "ZodError"
      },
      {
        "issues": [
          {
            "code": "invalid_union",
            "unionErrors": [
              {
                "issues": [
                  {
                    "code": "invalid_type",
                    "expected": "string",
                    "received": "null",
                    "path": [
                      "id"
                    ],
                    "message": "Expected string, received null"
                  }
                ],
                "name": "ZodError"
              },
              {
                "issues": [
                  {
                    "code": "invalid_type",
                    "expected": "number",
                    "received": "null",
                    "path": [
                      "id"
                    ],
                    "message": "Expected number, received null"
                  }
                ],
                "name": "ZodError"
              }
            ],
            "path": [
              "id"
            ],
            "message": "Invalid input"
          }
        ],
        "name": "ZodError"
      }
    ],
    "path": [],
    "message": "Invalid input"
  }
]
- [ ] Maintain comprehensive test coverage during refactors
- [ ] Build a lightweight web interface for unified calendar and task management
- [ ] Profile and optimize performance for large datasets
- [ ] Persist external ICS calendar URLs with aliases to avoid re-passing the full URL
- [ ] Ajustar retorno do list_events dos ICS para retornar compromissos detalhados e não apenas contagem
- [ ] Implementar adição de eventos em batch via arquivo ICS (importação em massa)
- [ ] Debug Cursor MCP client certificate compatibility com porta 8443 (atualmente via ZeroTier)
- [ ] Enable Nginx rate-limiting and fail2ban for brute-force protection
- [ ] Ship access/error logs to local file (debug-level) com logrotate policy
- [ ] Run dependency vulnerability scan (pip-audit) as CI step
- [ ] Document all steps in doc/guides/security_plan.md and link from README
