import multiprocessing as mp
import queue


def server_game_loop(client_commands):
    while True:
        try:
            msg = client_commands.get(True, 60)
            print(f"server-msg: {msg['text']}")

            # Implement proper rpc handling logic here
            #
            # if msg['method'] == 'login':
            #     do_login(msg)
            # elif msg['method'] == 'click_grid_pos':
            #     do_click_grid_position(msg)
            condition = msg['reply_to']['condition']
            response = msg['reply_to']['response']
            with condition:
                response.value = 'hello'
                condition.notify_all()
            # print(f"Message sent to client")
        except queue.Empty:
            # print("Timeout server will abort")
            return


def client_game_loop(client_commands, condition, reply_state):
    while True:
        client_commands.put({'text': 'Hello', 'reply_to': {'condition': condition, 'response': reply_state}})
        condition.acquire()

        if not condition.wait(1):
            print("Server is too lazy")
            continue

        print(f"server replied with: {reply_state.value}")

        # msg = server_responses.get()
        # print(f"Client-msg from server {msg}")


def main():
    with mp.Manager() as manager:
        # since value has to be one of
        # https://docs.python.org/3/library/array.html#module-array
        client_reply = manager.Value('u', '{}')
        condition = manager.Condition()

        client_commands = manager.Queue()

        server = mp.Process(target=server_game_loop, args=(client_commands,))
        server.daemon = True
        server.start()

        client = mp.Process(target=client_game_loop, args=(client_commands, condition, client_reply))
        client.daemon = True
        client.start()

        while True:
            server.join(1)
            client.join(1)


if __name__ == '__main__':
    main()
