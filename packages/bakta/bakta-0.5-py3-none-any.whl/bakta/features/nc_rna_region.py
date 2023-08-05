
import logging
import re
import subprocess as sp
from collections import OrderedDict

import bakta.config as cfg
import bakta.constants as bc

log = logging.getLogger('NC_RNA_REGION')


def predict_nc_rna_regions(genome, contigs_path):
    """Search for non-coding RNA regions."""

    output_path = cfg.tmp_path.joinpath('ncrna-regions.tsv')
    cmd = [
        'cmscan',
        '--noali',
        '--cut_tc',
        '-g',  # activate glocal mode
        '--nohmmonly',  # strictly use CM models
        '--rfam',
        '--cpu', str(cfg.threads),
        '--tblout', str(output_path)
    ]
    if(genome['size'] >= 1000000):
        cmd.append('-Z')
        cmd.append(str(2 * genome['size'] // 1000000))
    cmd.append(str(cfg.db_path.joinpath('ncRNA-regions')))
    cmd.append(str(contigs_path))
    log.debug('cmd=%s', cmd)
    proc = sp.run(
        cmd,
        cwd=str(cfg.tmp_path),
        env=cfg.env,
        stdout=sp.PIPE,
        stderr=sp.PIPE,
        universal_newlines=True
    )
    if(proc.returncode != 0):
        log.debug('stdout=\'%s\', stderr=\'%s\'', proc.stdout, proc.stderr)
        log.warning('ncRNA regions failed! cmscan-error-code=%d', proc.returncode)
        raise Exception(f'cmscan error! error code: {proc.returncode}')

    rfam2go = {}
    rfam2go_path = cfg.db_path.joinpath('rfam-go.tsv')
    with rfam2go_path.open() as fh:
        for line in fh:
            (rfam, go) = line.split('\t')
            if(rfam in rfam2go):
                rfam2go[rfam].append(go)
            else:
                rfam2go[rfam] = [go]

    ncrnas = []
    with output_path.open() as fh:
        for line in fh:
            if(line[0] != '#'):
                (subject, accession, contig_id, contig_acc, mdl, mdl_from, mdl_to,
                    start, stop, strand, trunc, passed, gc, bias, score, evalue,
                    inc, description) = re.split('\s+', line.strip(), maxsplit=17)
                
                if(strand == '-'):
                    (start, stop) = (stop, start)
                (start, stop) = (int(start), int(stop))
                evalue = float(evalue)
                length = stop - start + 1
                if(trunc == "5'"):
                    truncated = bc.FEATURE_END_5_PRIME
                elif(trunc == "3'"):
                    truncated = bc.FEATURE_END_3_PRIME
                else:
                    truncated = None
                
                if(evalue > 1E-4):
                    log.debug(
                        'discard low E value: contig=%s, start=%i, stop=%i, strand=%s, gene=%s, length=%i, truncated=%s, evalue=%1.1e',
                        contig_id, start, stop, strand, subject, length, truncated, evalue
                    )
                else:
                    rfam_id = f'RFAM:{accession}'
                    db_xrefs = [rfam_id]
                    if(rfam_id in rfam2go):
                        db_xrefs += rfam2go[rfam_id]
                    
                    ncrna_region = OrderedDict()
                    ncrna_region['type'] = bc.FEATURE_NC_RNA_REGION
                    ncrna_region['contig'] = contig_id
                    ncrna_region['start'] = start
                    ncrna_region['stop'] = stop
                    ncrna_region['strand'] = bc.STRAND_FORWARD if strand == '+' else bc.STRAND_REVERSE
                    ncrna_region['gene'] = subject

                    if(truncated is None):
                        ncrna_region['product'] = description
                    elif(truncated == bc.FEATURE_END_UNKNOWN):
                        ncrna_region['product'] = f'(partial) {description}'
                    elif(truncated == bc.FEATURE_END_5_PRIME):
                        ncrna_region['product'] = f"(5' truncated) {description}"
                    elif(truncated == bc.FEATURE_END_3_PRIME):
                        ncrna_region['product'] = f"(3' truncated) {description}"
                    
                    if(truncated):
                        ncrna_region['truncated'] = truncated
                    
                    ncrna_region['score'] = float(score)
                    ncrna_region['evalue'] = evalue
                    ncrna_region['db_xrefs'] = db_xrefs

                    ncrnas.append(ncrna_region)
                    log.info(
                        'contig=%s, start=%i, stop=%i, strand=%s, product=%s, length=%i, truncated=%s, evalue=%1.1e',
                        ncrna_region['contig'], ncrna_region['start'], ncrna_region['stop'], ncrna_region['strand'], ncrna_region['product'], length, truncated, ncrna_region['evalue']
                    )
    log.info('predicted=%i', len(ncrnas))
    return ncrnas
