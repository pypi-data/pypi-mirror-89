from bx.command import Command
import logging as log
from nibabel.freesurfer import io
import os.path as op
import bx


class SignatureCommand(Command):
    """Download composite measurements labeled as 'signatures' of Alzheimer's Disease

    Available subcommands:
     thickness:\t\tbased on FreeSurfer's cortical thickness
     grayvol:\t\tbased on FreeSurfer's local cortical gray matter volumes
     aging:\t\tbased on the aging signature described in Bakkour et al., 2013.

    Usage:
     bx signature <subcommand> <resource_id>

    Jack's and Dickerson's AD signatures are calculated in two versions,
    weighted and not weighted. Weighted means that the formula has been
    applied by normalizing each ROI value by local surface area (as explained
    in the papers).
    Not-weighted versions correspond to mean values across regions.

    Examples:

    `bx signature thickness` will return Jack's, Dickerson's and the aging
        signature, based on thickness values.
    `bx signature grayvol` will return Jack's and Dickerson's only, as the
        aging signature does not have any "grayvol" version.
    `bx signature aging` will return the aging signature only.

    References:
    - Jack et al., Alzheimers Dement. 2017
    - Dickerson et al., Neurology, 2011
    - Bakkour et al., NeuroImage, 2013
    """
    nargs = 2
    subcommands = ['thickness', 'grayvol', 'aging']

    def __init__(self, *args, **kwargs):
        super(SignatureCommand, self).__init__(*args, **kwargs)

    def parse(self):
        subcommand = self.args[0]
        id = self.args[1]  # should be a project or an experiment_id

        from bx import xnat
        experiments = xnat.collect_experiments(self.xnat, id, max_rows=10)

        if subcommand in ['thickness', 'grayvol']:
            d = {'thickness': 'ThickAvg', 'grayvol': 'GrayVol'}
            df = signatures(self.xnat, experiments, d[subcommand],
                            resource_name='FREESURFER6_HIRES')
            self.to_excel(id, df)
        elif subcommand in ['aging']:
            df = signatures(self.xnat, experiments, 'ThickAvg',
                            resource_name='FREESURFER6_HIRES')
            q = 'signature == "aging" & weighted'
            self.to_excel(id, df.query(q))


def __signature__(x, experiment_id, regions, weighted=True,
                  measurement='ThickAvg', resource_name='FREESURFER6_HIRES'):
    e = x.select.experiment(experiment_id)
    r = e.resource(resource_name)
    aparc = r.aparc()

    weighted_sum = 0
    total_surf_area = 0

    query = 'region == "{region}" & side == "{side}" & \
             measurement == "{measurement}"'

    for r in regions:
        for s in ['left', 'right']:
            q = query.format(region=r, side=s, measurement=measurement)
            thickness = float(aparc.query(q)['value'])

            q = query.format(region=r, side=s, measurement='SurfArea')
            surf_area = int(aparc.query(q)['value'])

            weighted_sum += thickness * surf_area if weighted else thickness
            total_surf_area += surf_area

    if weighted:
        final = weighted_sum / total_surf_area
    else:
        final = weighted_sum / (2 * len(regions))

    return final


def __aging_signature__(x, experiment_id, weighted=True, resource_name='FREESURFER6_HIRES'):
    import tempfile
    import os
    from glob import glob

    fh, fp = tempfile.mkstemp(suffix='.thickness')
    os.close(fh)
    e = x.select.experiment(experiment_id)
    r = e.resource(resource_name)

    # Cortical thickness map
    f = list(r.files('*lh.thickness'))[0]
    f.get(fp)
    lh_thickness = io.read_morph_data(fp)

    f = list(r.files('*rh.thickness'))[0]
    f.get(fp)
    rh_thickness = io.read_morph_data(fp)

    rois_path = op.join(op.dirname(op.dirname(bx.__file__)), 'data', 'labels')
    files = glob(op.join(rois_path, '*.label'))

    thickness_sum = 0
    n_regions = len(files)
    n_vertex = 0

    for f in files:
        thickness = 0
        filename = op.basename(f)
        roi = io.read_label(f)
        n_vertex += len(roi)
        if filename.startswith('rh'):
            for vertex in roi:
                thickness += rh_thickness[vertex]
        elif filename.startswith('lh'):
            for vertex in roi:
                thickness += lh_thickness[vertex]

        if weighted:
            thickness_sum += thickness
        else:
            thickness_sum += thickness / len(roi)

    if weighted:
        signature = thickness_sum / n_vertex
    else:
        signature = thickness_sum / n_regions

    return signature


def signature(x, experiment_id, measurement=None,
              resource_name='FREESURFER6_HIRES'):
    import pandas as pd

    columns = ['signature', 'weighted', 'measurement', 'value']
    table = []
    for sig in ['jack', 'dickerson']:
        for weighted in [False, True]:
            meas = ['ThickAvg', 'GrayVol']
            if measurement:
                meas = [measurement]
            for m in meas:
                if sig == 'jack':
                    regions = ['entorhinal', 'inferiortemporal', 'middletemporal',
                               'fusiform']
                    res = __signature__(x, experiment_id, regions, weighted, m,
                                        resource_name=resource_name)
                    row = [sig, weighted, m, res]
                    table.append(row)
                elif sig == 'dickerson':
                    regions = ['middletemporal', 'inferiortemporal', 'temporalpole',
                               'inferiorparietal', 'superiorfrontal', 'superiorparietal',
                               'supramarginal', 'precuneus', 'parstriangularis',
                               'parsopercularis', 'parsorbitalis']

                    res = __signature__(x, experiment_id, regions, weighted, m,
                                        resource_name=resource_name)
                    row = [sig, weighted, m, res]
                    table.append(row)

    if measurement != 'GrayVol':
        for weighted in [False, True]:
            # Aging signature
            res = __aging_signature__(x, experiment_id, weighted,
                                      resource_name='FREESURFER6_HIRES')
            row = ['aging', weighted, 'ThickAvg', res]
            table.append(row)

    return pd.DataFrame(table, columns=columns)


def signatures(x, experiments, measurement=None, resource_name='FREESURFER6_HIRES'):
    from tqdm import tqdm
    import pandas as pd

    table = []
    for e in tqdm(experiments):
        log.debug(e)
        try:
            s = e['subject_label']
            e_id = e['ID']
            volumes = signature(x, e_id, measurement=measurement,
                                resource_name=resource_name)

            volumes['subject'] = s
            volumes['ID'] = e['ID']
            table.append(volumes)
        except KeyboardInterrupt:
            return pd.concat(table).set_index('ID').sort_index()
        except Exception as exc:
            log.error('Failed for %s. Skipping it. (%s)' % (e, exc))

    data = pd.concat(table).set_index('ID').sort_index()
    return data
