from __future__ import absolute_import, print_function, unicode_literals
from builtins import dict, str
import logging
import indra.statements as ist

logger = logging.getLogger(__name__)


class EnglishAssembler(object):
    """This assembler generates English sentences from INDRA Statements.

    Parameters
    ----------
    stmts : Optional[list[indra.statements.Statement]]
        A list of INDRA Statements to be added to the assembler.

    Attributes
    ----------
    statements : list[indra.statements.Statement]
        A list of INDRA Statements to assemble.
    model : str
        The assembled sentences as a single string.
    stmt_agents : list[list[AgentWithCoordinates]]
        A list containing lists of AgentWithCoordinates objects for each of
        the assembled statements. Coordinates represent the location of
        agents in the model.
    """
    def __init__(self, stmts=None):
        if stmts is None:
            self.statements = []
        else:
            self.statements = stmts
        self.model = None
        self.stmt_agents = []

    def add_statements(self, stmts):
        """Add INDRA Statements to the assembler's list of statements.

        Parameters
        ----------
        stmts : list[indra.statements.Statement]
            A list of :py:class:`indra.statements.Statement`
            to be added to the statement list of the assembler.
        """
        self.statements += stmts

    def make_model(self):
        """Assemble text from the set of collected INDRA Statements.

        Returns
        -------
        stmt_strs : str
            Return the assembled text as unicode string. By default, the text
            is a single string consisting of one or more sentences with
            periods at the end.
        """
        stmt_strs = []
        # Keep track of current length of the model text.
        text_length = 0
        for stmt in self.statements:
            sb = None
            # Get a SentenceBuilder object per statement
            if isinstance(stmt, ist.Modification):
                sb = _assemble_modification(stmt)
            elif isinstance(stmt, ist.Autophosphorylation):
                sb = _assemble_autophosphorylation(stmt)
            elif isinstance(stmt, ist.Association):
                sb = _assemble_association(stmt)
            elif isinstance(stmt, ist.Complex):
                sb = _assemble_complex(stmt)
            elif isinstance(stmt, ist.Influence):
                sb = _assemble_influence(stmt)
            elif isinstance(stmt, ist.RegulateActivity):
                sb = _assemble_regulate_activity(stmt)
            elif isinstance(stmt, ist.RegulateAmount):
                sb = _assemble_regulate_amount(stmt)
            elif isinstance(stmt, ist.ActiveForm):
                sb = _assemble_activeform(stmt)
            elif isinstance(stmt, ist.Translocation):
                sb = _assemble_translocation(stmt)
            elif isinstance(stmt, ist.Gef):
                sb = _assemble_gef(stmt)
            elif isinstance(stmt, ist.Gap):
                sb = _assemble_gap(stmt)
            elif isinstance(stmt, ist.Conversion):
                sb = _assemble_conversion(stmt)
            else:
                logger.warning('Unhandled statement type: %s.' % type(stmt))
            if sb:
                stmt_strs.append(sb.sentence)
                # If this is not the first sentence, the agents coordinates
                # should be updated
                for ag in sb.agents:
                    ag.update_coords(text_length)
                self.stmt_agents.append(sb.agents)
                # Update the length of the text by adding the length of the new
                # sentence and a space.
                text_length += (len(sb.sentence) + 1)
            else:
                # If sentence wasn't built, add empty list of agents to keep
                # consistent structure with statements.
                self.stmt_agents.append([])
        if stmt_strs:
            return ' '.join(stmt_strs)
        else:
            return ''


class AgentWithCoordinates():
    """English representation of an agent.

    Parameters
    ----------
    agent_str : str
        Full English description of an agent.
    name : str
        Name of an agent.
    db_refs : dict
        Dictionary of database identifiers associated with this agent.
    coords : tuple(int)
        A tuple of integers representing coordinates of agent name in a text.
        If not provided, coords will be set to coordinates of name in
        agent_str. When AgentWithCoordinates is a part of SentenceBuilder or
        EnglishAssembler, the coords represent the location of agent name in
        the SentenceBuilder.sentence or EnglishAssembler.model.
    """
    def __init__(self, agent_str, name, db_refs, coords=None):
        self.agent_str = agent_str
        self.name = name
        self.db_refs = db_refs
        self.coords = coords if coords else (
            agent_str.find(name), agent_str.find(name) + len(name))

    def update_coords(self, shift_by):
        """Update coordinates by shifting them by a given number of characters.

        Parameters
        ----------
        shift_by : int
            How many characters to shift the parameters by.
        """
        current_coords = self.coords
        self.coords = (current_coords[0] + shift_by,
                       current_coords[1] + shift_by)

    def __repr__(self):
        return str(self)

    def __str__(self):
        return 'AgentWithCoordinates(%s (%s), coords=%s)' % (
            self.agent_str, self.name, self.coords)


class SentenceBuilder():
    """Builds a sentence from agents and strings.

    Attributes
    ----------
    agents : list[AgentWithCoordinates]
        A list of AgentWithCoordinates objects that are part of a sentence.
        The coordinates of the agent name are being dynamically updated as the
        sentence is being constructed.
    sentence : str
        A sentence that is being built by the builder.
    """
    def __init__(self):
        self.agents = []
        self.sentence = ''

    def append(self, element):
        """Append an element to the end of the sentence.

        Parameters
        ----------
        element : str or AgentWithCoordinates
            A string or AgentWithCoordinates object to be appended in the end
            of the sentence. Agent's name coordinates are updated relative to
            the current length of the sentence.
        """
        if isinstance(element, str):
            self.sentence += element
        elif isinstance(element, AgentWithCoordinates):
            element.update_coords(len(self.sentence))
            self.sentence += element.agent_str
            self.agents.append(element)

    def prepend(self, element):
        """Prepend an element to the beginning of the sentence.

        Parameters
        ----------
        element : str or AgentWithCoordinates
            A string or AgentWithCoordinates object to be added in the
            beginning of the sentence. All existing agents' names coordinates
            are updated relative to the new length of the sentence.
        """
        current_sentence = self.sentence
        if isinstance(element, str):
            self.sentence = element + current_sentence
            for ag in self.agents:
                ag.update_coords(len(element))
        elif isinstance(element, AgentWithCoordinates):
            self.sentence = element.agent_str + ' ' + current_sentence
            for ag in self.agents:
                ag.update_coords(len(element.agent_str) + 1)
            self.agents.insert(0, element)

    def append_as_list(self, lst, oxford=True):
        """Append a list of elements in a gramatically correct way.

        Parameters
        ----------
        lst : list[str] or list[AgentWithCoordinates]
            A list of elements to append. Elements in this list represent a
            sequence and grammar standards require the use of appropriate
            punctuation and conjunction to connect them (e.g. [ag1, ag2, ag3]).
        oxford : Optional[bool]
            Whether to use oxford grammar standards. Default: True
        """
        if len(lst) > 2:
            for el in lst[:-2]:
                self.append(el)
                self.append(', ')
            self.append(lst[-2])
            if oxford:
                self.append(',')
            self.append(' and ')
            self.append(lst[-1])
        elif len(lst) == 2:
            self.append(lst[0])
            self.append(' and ')
            self.append(lst[1])
        elif len(lst) == 1:
            self.append(lst[0])

    def append_as_sentence(self, lst):
        """Append a list of elements by concatenating them together.

        Note: a list of elements here are parts of sentence that do not
        represent a sequence and do not need to have extra punctuation or
        conjunction between them.

        Parameters
        ----------
        lst : list[str] or list[AgentWithCoordinates]
            A list of elements to append. Elements in this list do not
            represent a sequence and do not need to have extra punctuation or
            conjunction between them (e.g. [subj, ' is a GAP for ', obj]).
        """
        for el in lst:
            self.append(el)

    def make_sentence(self):
        """After the parts of a sentence are joined, create a sentence."""
        self.sentence = _make_sentence(self.sentence)


def _assemble_agent_str(agent):
    """Assemble an Agent object to AgentWithCoordinates object."""
    agent_str = agent.name

    # Only do the more detailed assembly for molecular agents
    if not isinstance(agent, ist.Agent):
        return AgentWithCoordinates(agent_str, agent.name, agent.db_refs)

    # Handle mutation conditions
    if agent.mutations:
        is_generic = False
        mut_strs = []
        for mut in agent.mutations:
            res_to = mut.residue_to if mut.residue_to else ''
            res_from = mut.residue_from if mut.residue_from else ''
            pos = mut.position if mut.position else ''
            mut_str = '%s%s%s' % (res_from, pos, res_to)
            # If this is the only mutation and there are no details
            # then this is a generic mutant
            if not mut_str and len(agent.mutations) == 1:
                is_generic = True
                break
            mut_strs.append(mut_str)
        if is_generic:
            agent_str = 'mutated ' + agent_str
        else:
            mut_strs = '/'.join(mut_strs)
            agent_str = '%s-%s' % (agent_str, mut_strs)

    # Handle location
    if agent.location is not None:
        agent_str += ' in the ' + agent.location

    if not agent.mods and not agent.bound_conditions and not agent.activity:
        return AgentWithCoordinates(agent_str, agent.name, agent.db_refs)

    # Handle bound conditions
    bound_to = [bc.agent.name for bc in
                agent.bound_conditions if bc.is_bound]
    not_bound_to = [bc.agent.name for bc in
                    agent.bound_conditions if not bc.is_bound]
    if bound_to:
        agent_str += ' bound to ' + _join_list(bound_to)
        if not_bound_to:
            agent_str += ' and not bound to ' +\
                _join_list(not_bound_to)
    else:
        if not_bound_to:
            agent_str += ' not bound to ' +\
                _join_list(not_bound_to)

    # Handle modification conditions
    if agent.mods:
        # Special case when we have a single modification without a position
        if len(agent.mods) == 1 and agent.mods[0].position is None:
            # First we get the modification state string like "phosphorylated"
            prefix = _mod_state_str(agent.mods[0].mod_type)
            # If there is a residue, we prefix the state with the name of the
            # residue.
            if agent.mods[0].residue is not None:
                residue_str =\
                    ist.amino_acids[agent.mods[0].residue]['full_name']
                prefix = residue_str + '-' + prefix
            # If there is no residue, we handle negatives by prefixing with
            # "un"
            elif not agent.mods[0].is_modified:
                prefix = 'un' + prefix
            # Ee add the modification before the agent
            agent_str = prefix + ' ' + agent_str
        else:
            if agent.bound_conditions:
                agent_str += ' and'
            agent_str += ' %s on ' % _mod_state_str(agent.mods[0].mod_type)
            mod_lst = []
            for m in agent.mods:
                if m.position is None:
                    if m.residue is not None:
                        residue_str =\
                            ist.amino_acids[m.residue]['full_name']
                        mod_lst.append(residue_str)
                    else:
                        mod_lst.append('an unknown residue')
                elif m.position is not None and m.residue is None:
                    mod_lst.append('amino acid %s' % m.position)
                else:
                    mod_lst.append(m.residue + m.position)
            agent_str += _join_list(mod_lst)

    # Handle activity conditions
    if agent.activity is not None:
        # Get the modifier specific to the activity type, if any
        pre_prefix = \
            activity_type_prefix.get(agent.activity.activity_type, '')
        if agent.activity.is_active:
            prefix = pre_prefix + 'active'
        else:
            # See if there is a special override for the inactive form
            if agent.activity.activity_type in inactivity_type_prefix_override:
                pre_prefix = inactivity_type_prefix_override[
                    agent.activity.activity_type]
            prefix = pre_prefix + 'inactive'
        agent_str = prefix + ' ' + agent_str

    return AgentWithCoordinates(agent_str, agent.name, agent.db_refs)


def english_join(lst):
    """Join a list of strings according to English grammar.

    Parameters
    ----------
    lst : list of str
        A list of strings to join.

    Returns
    -------
    str
        A string which describes the list of elements, e.g.,
        "apples, pears, and bananas".
    """
    return _join_list(lst, oxford=True)


def _join_list(lst, oxford=True):
    """Join a list of words in a grammatically correct way."""
    if len(lst) > 2:
        s = ', '.join(lst[:-1])
        if oxford:
            s += ','
        s += ' and ' + lst[-1]
    elif len(lst) == 2:
        s = lst[0] + ' and ' + lst[1]
    elif len(lst) == 1:
        s = lst[0]
    else:
        s = ''
    return s


def _assemble_activeform(stmt):
    """Assemble ActiveForm statements into SentenceBuilder object."""
    subj_str = _assemble_agent_str(stmt.agent)
    sb = SentenceBuilder()
    sb.append(subj_str)
    if stmt.is_active:
        is_active_str = 'active'
    else:
        is_active_str = 'inactive'
    if stmt.activity == 'activity':
        sb.append(' is ')
    elif stmt.activity == 'kinase':
        sb.append(' is kinase-')
    elif stmt.activity == 'phosphatase':
        sb.append(' is phosphatase-')
    elif stmt.activity == 'catalytic':
        sb.append(' is catalytically ')
    elif stmt.activity == 'transcription':
        sb.append(' is transcriptionally ')
    elif stmt.activity == 'gtpbound':
        sb.append(' is GTP-bound ')
    sb.append(is_active_str)
    sb.make_sentence()
    return sb


def _assemble_modification(stmt):
    """Assemble Modification statements into SentenceBuilder object."""
    sub_str = _assemble_agent_str(stmt.sub)
    sb = SentenceBuilder()
    if stmt.enz is not None:
        enz_str = _assemble_agent_str(stmt.enz)
        if _get_is_direct(stmt):
            mod_str = ' ' + _mod_process_verb(stmt) + ' '
        else:
            mod_str = ' leads to the ' + _mod_process_noun(stmt) + ' of '
        sb.append_as_sentence([enz_str, mod_str, sub_str])
    else:
        sb.append_as_sentence([sub_str, ' is ', _mod_state_stmt(stmt)])

    if stmt.residue is not None:
        if stmt.position is None:
            mod_str = ' on ' + ist.amino_acids[stmt.residue]['full_name']
        else:
            mod_str = ' on ' + stmt.residue + stmt.position
    elif stmt.position is not None:
        mod_str = ' at position %s' % stmt.position
    else:
        mod_str = ''
    sb.append(mod_str)
    sb.make_sentence()
    return sb


def _assemble_association(stmt):
    """Assemble Association statements into SentenceBuilder object."""
    member_strs = [_assemble_agent_str(m.concept) for m in stmt.members]
    sb = SentenceBuilder()
    sb.append(member_strs[0])
    sb.append(' is associated with ')
    sb.append_as_list(member_strs[1:])
    sb.make_sentence()
    return sb


def _assemble_complex(stmt):
    """Assemble Complex statements into SentenceBuilder object."""
    member_strs = [_assemble_agent_str(m) for m in stmt.members]
    sb = SentenceBuilder()
    sb.append(member_strs[0])
    sb.append(' binds ')
    sb.append_as_list(member_strs[1:])
    sb.make_sentence()
    return sb


def _assemble_autophosphorylation(stmt):
    """Assemble Autophosphorylation statements into SentenceBuilder object."""
    enz_str = _assemble_agent_str(stmt.enz)
    sb = SentenceBuilder()
    sb.append(enz_str)
    sb.append(' phosphorylates itself')
    if stmt.residue is not None:
        if stmt.position is None:
            mod_str = ' on ' + ist.amino_acids[stmt.residue]['full_name']
        else:
            mod_str = ' on ' + stmt.residue + stmt.position
    else:
        mod_str = ''
    sb.append(mod_str)
    sb.make_sentence()
    return sb


def _assemble_regulate_activity(stmt):
    """Assemble RegulateActivity statements into SentenceBuilder object."""
    subj_str = _assemble_agent_str(stmt.subj)
    obj_str = _assemble_agent_str(stmt.obj)
    if stmt.is_activation:
        rel_str = ' activates '
    else:
        rel_str = ' inhibits '
    sb = SentenceBuilder()
    sb.append_as_sentence([subj_str, rel_str, obj_str])
    sb.make_sentence()
    return sb


def _assemble_regulate_amount(stmt):
    """Assemble RegulateAmount statements into SentenceBuilder object."""
    obj_str = _assemble_agent_str(stmt.obj)
    sb = SentenceBuilder()
    if stmt.subj is not None:
        subj_str = _assemble_agent_str(stmt.subj)
        if isinstance(stmt, ist.IncreaseAmount):
            rel_str = ' increases the amount of '
        elif isinstance(stmt, ist.DecreaseAmount):
            rel_str = ' decreases the amount of '
        sb.append_as_sentence([subj_str, rel_str, obj_str])
    else:
        sb.append(obj_str)
        if isinstance(stmt, ist.IncreaseAmount):
            sb.append(' is produced')
        elif isinstance(stmt, ist.DecreaseAmount):
            sb.append(' is degraded')
    sb.make_sentence()
    return sb


def _assemble_translocation(stmt):
    """Assemble Translocation statements into SentenceBuilder object."""
    agent_str = _assemble_agent_str(stmt.agent)
    sb = SentenceBuilder()
    sb.append_as_sentence([agent_str, ' translocates'])
    if stmt.from_location is not None:
        sb.append_as_sentence([' from the ', stmt.from_location])
    if stmt.to_location is not None:
        sb.append_as_sentence([' to the ', stmt.to_location])
    sb.make_sentence()
    return sb


def _assemble_gap(stmt):
    """Assemble Gap statements into SentenceBuilder object."""
    subj_str = _assemble_agent_str(stmt.gap)
    obj_str = _assemble_agent_str(stmt.ras)
    sb = SentenceBuilder()
    sb.append_as_sentence([subj_str, ' is a GAP for ', obj_str])
    sb.make_sentence()
    return sb


def _assemble_gef(stmt):
    """Assemble Gef statements into SentenceBuilder object."""
    subj_str = _assemble_agent_str(stmt.gef)
    obj_str = _assemble_agent_str(stmt.ras)
    sb = SentenceBuilder()
    sb.append_as_sentence([subj_str, ' is a GEF for ', obj_str])
    sb.make_sentence()
    return sb


def _assemble_conversion(stmt):
    """Assemble a Conversion statement into SentenceBuilder object."""
    reactants = [_assemble_agent_str(r) for r in stmt.obj_from]
    products = [_assemble_agent_str(r) for r in stmt.obj_to]
    sb = SentenceBuilder()
    if stmt.subj is not None:
        subj_str = _assemble_agent_str(stmt.subj)
        sb.append(subj_str)
        sb.append(' catalyzes the conversion of ')
        sb.append_as_list(reactants)
        sb.append(' into ')
        sb.append_as_list(products)
    else:
        sb.append_as_list(reactants)
        sb.append(' is converted into ')
        sb.append_as_list(products)
    sb.make_sentence()
    return sb


def _assemble_influence(stmt):
    """Assemble an Influence statement into SentenceBuilder object."""
    subj_str = _assemble_agent_str(stmt.subj.concept)
    obj_str = _assemble_agent_str(stmt.obj.concept)

    sb = SentenceBuilder()
    # Note that n is prepended to increase to make it "an increase"
    if stmt.subj.delta.polarity is not None:
        subj_delta_str = ' decrease' if stmt.subj.delta.polarity == -1 \
            else 'n increase'
        sb.append_as_sentence(['a', subj_delta_str, ' in ', subj_str])
    else:
        sb.append(subj_str)

    sb.append(' causes ')

    if stmt.obj.delta.polarity is not None:
        obj_delta_str = ' decrease' if stmt.obj.delta.polarity == -1 \
            else 'n increase'
        sb.append_as_sentence(['a', obj_delta_str, ' in ', obj_str])
    else:
        sb.append(obj_str)

    sb.make_sentence()
    return sb


def _make_sentence(txt):
    """Make a sentence from a piece of text."""
    # Make sure first letter is capitalized
    txt = txt.strip(' ')
    txt = txt[0].upper() + txt[1:] + '.'
    return txt


def _get_is_direct(stmt):
    """Return True if there is any evidence that the statement is direct.

    If any of the evidences associated with the statement
    indicates a direct interaction then we assume the interaction
    is direct. If there is no evidence for the interaction being indirect
    then we default to direct.
    """
    any_indirect = False
    for ev in stmt.evidence:
        if ev.epistemics.get('direct') is True:
            return True
        elif ev.epistemics.get('direct') is False:
            # This guarantees that we have seen at least
            # some evidence that the statement is indirect
            any_indirect = True
    if any_indirect:
        return False
    return True


def _get_is_hypothesis(stmt):
    """Return True if there is only evidence that the statement is hypothetical.

    If all of the evidences associated with the statement
    indicate a hypothetical interaction then we assume the interaction
    is hypothetical.
    """
    for ev in stmt.evidence:
        if not ev.epistemics.get('hypothesis') is True:
            return True
    return False


def _get_is_hypothesis_adverb(stmt):
    """Return the string associated with a statement being hypothetical."""
    if _get_is_hypothesis(stmt):
        return ' hypothetically '
    else:
        return ''


def _mod_process_verb(stmt):
    # Example: Phosphorylation -> phosphorylates
    mod_name = stmt.__class__.__name__.lower()
    return statement_present_verb(mod_name)


def _mod_process_noun(stmt):
    # Example: Phosphorylation -> phosphorylation
    mod_name = stmt.__class__.__name__.lower()
    return mod_name


def _mod_state_stmt(stmt):
    # Example: Phosphorylation -> phosphorylated
    mod_name = stmt.__class__.__name__.lower()
    return statement_passive_verb(mod_name)


def _mod_state_str(s):
    return statement_passive_verb(s)


def statement_passive_verb(stmt_type):
    """Return the passive / state verb form of a statement type.

    Parameters
    ----------
    stmt_type : str
        The lower case string form of a statement type, for instance,
        'phosphorylation'.

    Returns
    -------
    str
        The passive/state verb form of a statement type, for instance,
        'phosphorylated'.
    """
    override = {
        'complex': 'bound',
        'regulateamount': 'amount regulated',
        'decreaseamount': 'decreased',
        'increaseamount': 'increased',
        'gap': 'GAP-regulated',
        'gef': 'GEF-regulated',
        'gtpactivation': 'GTP-activated',
        'influence': 'influenced',
        'event': 'happened',
        'conversion': 'converted',
        'modification': 'modified',
        'addmodification': 'modified',
        'removemodification': 'unmodified',
        'regulateactivity': 'activity regulated',
    }
    return override.get(stmt_type) if stmt_type in override else \
        stmt_type[:-3] + 'ed'


def statement_present_verb(stmt_type):
    """Return the present verb form of a statement type.

    Parameters
    ----------
    stmt_type : str
        The lower case string form of a statement type, for instance,
        'phosphorylation'.

    Returns
    -------
    str
        The present verb form of a statement type, for instance,
        'phosphorylates'.
    """
    override = {
        'complex': 'binds',
        'regulateamount': 'regulates the amount of',
        'increaseamount': 'increases the amount of',
        'decreaseamount': 'decreases the amount of',
        'gef': 'acts as a GEF for',
        'gap': 'acts as a GAP for',
        'inhibition': 'inhibits',
        'gtpactivation': 'activates when bound to GTP',
        'regulateactivity': 'regulates the activity of',
        'activeform': 'has active form',
        'conversion': 'converts',
        'influence': 'influences',
        'modification': 'modifies',
        'addmodification': 'adds a modification to',
        'removemodification': 'removes a modification of',
        'selfmodification': 'modifies itself',
        'event': 'happens'
    }
    return override.get(stmt_type) if stmt_type in override else \
        stmt_type[:-3] + 'es'


def statement_base_verb(stmt_type):
    """Return the base verb form of a statement type.

    Parameters
    ----------
    stmt_type : str
        The lower case string form of a statement type, for instance,
        'phosphorylation'.

    Returns
    -------
    str
        The base verb form of a statement type, for instance, 'phosphorylate'.
    """
    override = {
        'complex': 'bind',
        'regulateamount': 'regulate the amount of',
        'increaseamount': 'increase the amount of',
        'decreaseamount': 'decrease the amount of',
        'gef': 'act as a GEF for',
        'gap': 'act as a GAP for',
        'inhibition': 'inhibit',
        'gtpactivation': 'activate when bound to GTP',
        'regulateactivity': 'regulate the activity of',
        'activeform': 'have active form',
        'conversion': 'convert',
        'influence': 'influence',
        'modification': 'modify',
        'addmodification': 'add a modification to',
        'removemodification': 'remove a modification of',
        'selfmodification': 'modify itself',
        'event': 'happen'
    }
    return override.get(stmt_type) if stmt_type in override \
        else stmt_type[:-3] + 'e'


activity_type_prefix = {
    'catalytic': 'catalytically ',
    'gap': 'GAP-',
    'gef': 'GEF-',
    'gtpbound': 'GTP-bound ',
    'kinase': 'kinase-',
    'phosphatase': 'phosphatase-',
    'transcription': 'transcriptionally ',
    }


inactivity_type_prefix_override = {
    'gtpbound': 'GDP-bound ',
    }
