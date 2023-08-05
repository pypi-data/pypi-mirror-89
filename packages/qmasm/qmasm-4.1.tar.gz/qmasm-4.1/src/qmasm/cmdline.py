###################################
# Parse the QMASM command line    #
# By Scott Pakin <pakin@lanl.gov> #
###################################

import argparse
import re
import shlex
import string
import sys

class ParseCommandLine(object):
    def parse_command_line(self):
        "Parse the QMASM command line.  Return an argparse.Namespace."

        # Define all of our command-line arguments.
        cl_parser = argparse.ArgumentParser(description="Assemble a symbolic Hamiltonian into a numeric one")
        cl_parser.add_argument("input", nargs="*",
                               help="file(s) from which to read a symbolic Hamiltonian")
        cl_parser.add_argument("-v", "--verbose", action="count", default=0,
                               help="increase output verbosity (can be specified repeatedly)")
        cl_parser.add_argument("--run", action="store_true",
                               help="run the program on the current solver")
        cl_parser.add_argument("-o", "--output", metavar="FILE", default="<stdout>",
                               help="file to which to write weights and strengths (default: none)")
        cl_parser.add_argument("-O", type=int, nargs="?", const=1, default=0,
                               metavar="LEVEL",
                               help="optimize the layout; at -O1, remove unnecessary qubits")
        cl_parser.add_argument("--pin", action="append",
                               help="pin a set of qubits to a set of true or false values")
        cl_parser.add_argument("--format", choices=["qubist", "ocean", "qbsolv", "qmasm", "minizinc", "bqpjson"], default="qubist",
                               help="output-file format")
        cl_parser.add_argument("--values", choices=["bools", "ints"], default="bools",
                               help="output solution values as Booleans or integers (default: bools)")
        cl_parser.add_argument("--profile", type=str, default=None, metavar="NAME",
                               help="Profile name from dwave.conf to use")
        cl_parser.add_argument("--solver", type=str, default=None, metavar="NAME",
                               help='Solver name from dwave.conf to use or one of the special names "exact", "sim-anneal", "tabu", "kerberos[,<solver>]", or "qbsolv[,<solver>]"')
        cl_parser.add_argument("--chain-strength", metavar="NEG_NUM", type=float,
                               help="negative-valued chain strength (default: automatic)")
        cl_parser.add_argument("--pin-weight", metavar="NEG_NUM", type=float,
                               help="negative-valued pin weight (default: automatic)")
        cl_parser.add_argument("--qubo", action="store_true",
                               help="where supported, produce output files in QUBO rather than Ising format")
        cl_parser.add_argument("--samples", metavar="POS_INT", type=int, default=1000,
                               help="number of samples to take (default: 1000)")
        cl_parser.add_argument("--anneal-time", metavar="POS_INT", type=int, default=None,
                               help="annealing time in microseconds (default: automatic)")
        cl_parser.add_argument("--spin-revs", metavar="POS_INT", type=int, default=0,
                               help="number of spin-reversal transforms to perform (default: 0)")
        cl_parser.add_argument("--topology-file", default=None, metavar="FILE",
                               help="name of a file describing the topology (list of vertex pairs)")
        cl_parser.add_argument("--postproc", choices=["none", "sample", "opt"],
                               default="none",
                               help='type of postprocessing to perform (default: "none")')
        cl_parser.add_argument("--show", choices=["valid", "all", "best"], default="valid",
                               help='show valid solutions, all solutions, or the best (even if invalid) solutions (default: "valid")')
        cl_parser.add_argument("--always-embed", action="store_true",
                               help="when writing an output file, embed the problem in the physical topology even when not required (default: false)")
        cl_parser.add_argument("--composites", metavar="COMP1,COMP2,...",
                               default="",
                               help='wrap the solver within one or more composites (currently only "virtualgraph")')
        cl_parser.add_argument("--pack-qubits", metavar="POS_INT", type=int,
                               help='attempt to pack the problem into an N-qubit "corner" of the physical topology during embedding')
        cl_parser.add_argument("--physical", action="store_true",
                               help="map variables containing a number to the physical qubits represented by that number")
        cl_parser.add_argument("--schedule", metavar="T,S,...", type=str,
                               help="specify an annealing schedule as alternating lists of times (microseconds) and annealing fractions (0.0 to 1.0)")

        # Parse the command line.
        cl_args = cl_parser.parse_args()

        # Perform a few sanity checks on the parameters.
        if cl_args.chain_strength != None and cl_args.chain_strength >= 0.0:
            self.warn("A non-negative chain strength (%.20g) was specified\n" % cl_args.chain_strength)
        if cl_args.pin_weight != None and cl_args.pin_weight >= 0.0:
            self.warn("A non-negative pin strength (%.20g) was specified\n" % cl_args.pin_weight)
        if cl_args.spin_revs > cl_args.samples:
            self.abend("The number of spin reversals is not allowed to exceed the number of samples")
        self.parse_composite_string(cl_args.composites)  # Check for errors and discard the result.
        self.parse_anneal_sched_string(cl_args.schedule)  # Check for errors and discard the result.
        return cl_args

    def parse_composite_string(self, cstr):
        "Split the composites string into a list.  Abort on error."
        comps = []
        if cstr == "":
            return comps
        for c in cstr.split(","):
            if c == "virtualgraph":
                comps.append("VirtualGraph")
            else:
                self.abend('Unrecognized composite "%s"' % c)
        return comps

    def parse_anneal_sched_string(self, astr):
        "Parse an annealing schedule into a list of (time, frac) tuples."
        if astr == None:
            return None
        num_re = re.compile(r'[-+Ee.\d]+')  # All characters that can appear in a floating-point-number
        nums = num_re.findall(astr)
        if len(nums)%2 == 1:
            self.abend('Failed to parse "%s" as alternating times and annealing fractions' % astr)
        sched = []
        for i in range(0, len(nums), 2):
            try:
                t = float(nums[i])
            except ValueError:
                self.abend('Failed to parse "%s" as a floating-point number' % nums[i])
            try:
                s = float(nums[i + 1])
            except ValueError:
                self.abend('Failed to parse "%s" as a floating-point number' % nums[i + 1])
            sched.append((t, s))
        if len(sched) < 2:
            self.abend('Failed to parse "%s" into two or more (time, frac) pairs' % astr)
        return sched

    def get_command_line(self):
        "Return the command line as a string, properly quoted."
        return " ".join([shlex.quote(a) for a in sys.argv])

    def report_command_line(self, cl_args):
        "For provenance and debugging purposes, report our command line parameters."
        # Output the command line as is.
        verbosity = cl_args.verbose
        if verbosity < 1:
            return
        sys.stderr.write("Command line provided:\n\n")
        sys.stderr.write("    %s\n\n" % self.get_command_line())

        # At higher levels of verbosity, output every single option.
        if verbosity < 2:
            return
        sys.stderr.write("All QMASM parameters:\n\n")
        params = vars(cl_args)
        klen = max([len(a) for a in params.keys()])
        klen = max(klen + 2, len("Option"))   # +2 for "--"
        vlen = max([len(repr(a)) for a in params.values()])
        klen = max(vlen, len("Value(s)"))
        sys.stderr.write("    %-*s  %-*s\n" % (klen, "Option", vlen, "Value(s)"))
        sys.stderr.write("    %s  %s\n" % ("-" * klen, "-" * vlen))
        for k in sorted(params.keys()):
            kname = k.replace("_", "-")
            sys.stderr.write("    %-*s  %-*s\n" % (klen, "--" + kname, vlen, repr(params[k])))
        sys.stderr.write("\n")
