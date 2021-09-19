class Edge:
    def __init__(self, from_state: str, to_state: str, value: str) -> None:
        self.from_state = from_state
        self.to_state = to_state
        self.value = value

    def __str__(self) -> str:
        return f'Edge: {self.from_state} ----{self.value}----> {self.to_state}'

class Graph:
    def __init__(self, edges=[Edge], start_state='', accepted_states=[str]) -> None:
        self.edges = edges
        self.start_state = start_state
        self.accepted_states = accepted_states
        self.states = []
        self._update_states()

    def add_edge(self, edge: Edge) -> None:
        # Check that edge does not already exist
        for e in self.edges:
            if edge.from_state == e.from_state and edge.to_state == e.to_state and edge.value == e.value:
                return
        self.edges.append(edge)
        return

    def _update_states(self):
        for edge in self.edges:
            if edge.from_state not in self.states:
                self.states.append(edge.from_state)
            if edge.to_state not in self.states:
                self.states.append(edge.to_state)
        return
    
    def __str__(self):
        s = ""
        for edge in self.edges:
            s += f"  {edge}\n"
        return f'States: {", ".join(self.states)}\nAccepted States: {", ".join(self.accepted_states)}\nEdges:\n{s}'

    def get_edges(self, state: str):
        """
        Returns all outgoing edges for a given state
        """
        edges = []
        for edge in self.edges:
            if edge.from_state == state:
                edges.append(edge)
        return edges

    def travel(self, input: str, show_steps=True) -> bool:
        """
        Returns True if accepted, False if rejected, and None if
        travel was incomplete.
        """
        i = 0
        length = len(input)
        prev_state = None
        cur_state = self.start_state
        while i < length and cur_state:
            prev_state = cur_state
            cur_state = self._move(cur_state, input[i])

            if show_steps:
                print(f'Step {i}: {prev_state} ----{input[i]}----> {cur_state}')
            i += 1

        if not cur_state:
            if show_steps:
                print(f"State {prev_state} has no outgoing edge with value {input[i - 1]}")
            
            print("Graph was unable to complete travel. (Failed)")
            return None
        else:
            result = cur_state in self.accepted_states
            print(f'Final State {cur_state} Accepted = {cur_state in self.accepted_states}')
            return result

    def test_all_binary(self, num_bits=4, show_steps=False, padding=True):
        i = 0
        accepted = 0
        rejected = 0
        failed = 0
        for _ in range(2**num_bits):
            input = bin(i)[2:]
            if padding:
                input = '0' * (num_bits - len(input)) + input
            if show_steps:
                print('{:<{n}}'.format(input + ':', n=num_bits + 2))
            else:
                print('{:<{n}}'.format(input + ':', n=num_bits + 2), end='')

            result = self.travel(input, show_steps=show_steps)
            
            if show_steps:
                print('-' * 30)
            if result is None:
                failed += 1
            elif result is True:
                accepted += 1
            elif result is False:
                rejected += 1
            i += 1

        print(f"Overall Results: {accepted}/{accepted + rejected} accepted")
        print(f"{failed} inputs failed")

    def _move(self, cur_state: str, input) -> str:
        edges = self.get_edges(cur_state)
        for edge in edges:
            if edge.value == input:
                return edge.to_state
        return None

