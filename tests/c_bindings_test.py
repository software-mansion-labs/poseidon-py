import pytest

from poseidon_py.c_bindings import hades_permutation, UINT256_MAX


@pytest.mark.parametrize(
    "values, expected_result",
    [
        (
            [0, 0, 0],
            [
                3446325744004048536138401612021367625846492093718951375866996507163446763827,
                1590252087433376791875644726012779423683501236913937337746052470473806035332,
                867921192302518434283879514999422690776342565400001269945778456016268852423,
            ],
        ),
        (
            [1, 2, 3],
            [
                442682200349489646213731521593476982257703159825582578145778919623645026501,
                2233832504250924383748553933071188903279928981104663696710686541536735838182,
                2512222140811166287287541003826449032093371832913959128171347018667852712082,
            ],
        ),
        (
            [
                1590252087433376791875644726012779423683501236913937337746052470473806035331,
                0,
                1,
            ],
            [
                2816315091890306244152051356354735623185799741340363242687723926588581097926,
                1174388024304906333251735882349920869241523602186998163898648402150953320905,
                3130179701777278346489736877307607692841443146569701366557268590323003157201,
            ],
        ),
        (
            [
                1590252087433376791875644726012779423683501236913937337746052470473806035331,
                867921192302518434283879514999422690776342565400001269945778456016268852422,
                2,
            ],
            [
                2466701774179185519722078951105424092175312593851018652031455769946650344890,
                2352243219207232648751929626368027159089646561838637543238086846420810074454,
                3575805241161697265067819954489552738154756615397261208702965583009055491758,
            ],
        ),
        (
            [
                43251436235347542643274,
                35246236432545463564265,
                234724572654366437254274,
            ],
            [
                1575317031406813687724518246540075260292628078796896319476024584111151080566,
                1881749349821485077283454164949781990029379538746570850488875971763643895967,
                3379489860261142300861388663571723742013023150462788192386628889429951775269,
            ],
        ),
        (
            [
                1575317031406813687724518246540075260292628078796896319476024584111151080566,
                1881749349821485077283454164949781990029379538746570850488875971763643895967,
                3379489860261142300861388663571723742013023150462788192386628889429951775269,
            ],
            [
                403297634695272827073453812922874692973917040589234837032542390658827496456,
                2623267429533864024234137680111654922032331951552114930532975316480767922663,
                1700010063817349690466649548246055303909794025645929558037843943753543735930,
            ],
        ),
    ],
)
def test_hades_permutation(values, expected_result):
    result = hades_permutation(values=values)

    assert result == expected_result


@pytest.mark.parametrize("values", [[], [1], [1, 2], [1, 2, 3, 4]])
def test_invalid_values_length(values):
    with pytest.raises(ValueError):
        _ = hades_permutation(values=values)


@pytest.mark.parametrize(
    "values",
    [
        [1, 2, -3],
        [0, -1, 0],
        [UINT256_MAX + 1, UINT256_MAX, UINT256_MAX],
    ],
)
def test_invalid_value(values):
    with pytest.raises(ValueError):
        _ = hades_permutation(values=values)