import sys
import time
import json
import requests
import src.core.cancel_utils as cancel_utils
import pytest

# Adiciona um timeout global padrão para todos os testes, pode ser sobrescrito
# pelo decorator @pytest.mark.timeout em testes individuais.
# Você pode querer mover isso para um arquivo conftest.py se aplicável a muitos testes.
# pytest_plugins = ["pytest_timeout"]

@pytest.mark.timeout(30)  # Set a timeout of 30 seconds for this test
def test_sse_stream_read(url=None, timeout=10, event_timeout=20):
    try:
        url = cancel_utils.get_sse_url(url)
    except RuntimeError as e:
        print(str(e))
        pytest.fail(f"Failed to get SSE URL: {e}") # Falha explícita se não conseguir URL
        return

    headers = {"Accept": "text/event-stream", "Cache-Control": "no-cache"}
    sse_response = None
    try:
        get_session = requests.Session()
        # O timeout aqui ainda é para conexão e inatividade entre bytes
        sse_response = get_session.get(url, headers=headers, stream=True, timeout=(10, event_timeout))
        print(f"SSE stream status: {sse_response.status_code}")
        if sse_response.status_code != 200:
            pytest.fail(f"Error: Unexpected status code {sse_response.status_code}") # Falha explícita em status inesperado
            return
        print("SSE stream open, waiting for events")

        # Flags para verificar se os eventos esperados foram recebidos
        hello_received = False
        tools_list_received = False

        start_time = time.time()
        # Define um tempo limite para a leitura dos eventos iniciais
        # Isso é separado do timeout total do pytest, focado na lógica do teste
        event_reception_timeout = 15 # Tempo em segundos para esperar pelos eventos iniciais

        for line in sse_response.iter_lines():
            # Verificar se o tempo para receber os eventos iniciais excedeu o limite
            if not (hello_received and tools_list_received) and (time.time() - start_time > event_reception_timeout):
                 pytest.fail(f"Did not receive expected initial events within {event_reception_timeout} seconds.")
                 break # Sai do loop se exceder o tempo de espera pelos eventos iniciais

            if line:
                try:
                    text = line.decode("utf-8")
                    if text.startswith("event:"):
                        event_name = text[6:].strip()
                        print(f"Event name: {event_name}")
                        if event_name == "mcp/hello":
                            hello_received = True
                        elif event_name == "tools/list":
                            tools_list_received = True

                    elif text.startswith("data:"):
                        data = text[5:].strip()
                        print(f"Data: {data[:50]}{'...' if len(data) > 50 else ''}")

                    elif text.startswith(":"):
                        print("Heartbeat")
                        # Se ambos os eventos esperados já foram recebidos, podemos parar de ler
                        if hello_received and tools_list_received:
                            print("Received all expected initial events. Stopping stream read.")
                            break # Sai do loop após receber os eventos esperados

                    elif text == "":
                        print("End of event block")
                    else:
                        print(f"Unknown SSE line format: {text}")

                    # Se ambos os eventos foram recebidos, saia do loop principal
                    if hello_received and tools_list_received:
                        break

                except UnicodeDecodeError:
                    print(f"Binary data received (couldn't decode as UTF-8): {line}")
                except json.JSONDecodeError:
                    print(f"Failed to decode data as JSON for line: {text}")
                except Exception as e:
                    print(f"An error occurred while processing line: {str(e)}")
                    # Decida se um erro de processamento deve falhar o teste imediatamente
                    # pytest.fail(f"Error processing line: {e}")


        # Verificar se ambos os eventos esperados foram recebidos no final do loop
        if not (hello_received and tools_list_received):
             pytest.fail("Exited stream reading loop before receiving all expected initial events.")


    except requests.exceptions.Timeout:
        # Este timeout pega o timeout de conexão ou o timeout de inatividade entre bytes
        pytest.fail(f"Request timed out after {timeout} seconds (inactivity timeout).")
    except Exception as e:
        # Captura outras exceções gerais durante a conexão ou leitura antes do loop iter_lines
        pytest.fail(f"An error occurred during stream setup or initial reading: {str(e)}")

    finally:
        if sse_response:
            sse_response.close()
            print("SSE stream closed")

if __name__ == "__main__":
    # Este bloco é para execução direta do script, não é usado pelo pytest
    # Manter para compatibilidade se você executar o script diretamente
    arg_url = sys.argv[1] if len(sys.argv) > 1 else None
    # Para rodar com pytest, você usaria o comando pytest no terminal
    # Se quiser testar o código modificado diretamente, pode chamar a função:
    # test_sse_stream_read(arg_url) # Comente esta linha se sempre rodar com pytest
    print("Please run this using pytest for proper test execution and timeout handling.") 